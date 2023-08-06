response_body=/tmp/bb-response.json
token_filepath=~/.bb-tokens.json

_http_get() {
    # Execute HTTP GET request to given URL
    # Args: URL
    _http_request GET "$@"
}

_http_post() {
    # Execute HTTP POST request to given URL. Any additional arguments are
    # forwarded to _http_request
    # Args: URL [CURL-OPTIONS]
    _http_request POST "$@"
}

_http_request() {
    # Execute HTTP request of specified method (upper-case name) to given URL.
    # Any additional arguments are forwarded to curl.
    # The response is written to $response_body.
    # If a 401 response is returned, refresh access token, and repeat request.
    # Args: METHOD URL [CURL-OPTIONS]
    # Return: 0 if response ok
    #         1 if error in response
    #         2 if refreshing access failed

    local method url rc access_token http_status
    method="$1";  shift
    url="$1"; shift

    access_token=$(jq -r .access_token $token_filepath)

    http_status=$(curl -X "$method" -sL \
        -w "%{http_code}" \
        -o $response_body \
        -H 'Content-Type: application/json' \
        -H "Authorization: Bearer {$access_token}" \
        "$@" \
        "$url"
    )

    if [ "$http_status" -lt 300 ]; then
        rc=0

    elif [ "$http_status" -eq 401 ]; then
        if _bb_refresh_access; then
            _http_request "$method" "$url" "$@"
            rc=$?
        else
            rc=2
        fi

    else
        printf "Error (%s): " "$http_status" >&2
        # Display error message if response is valid JSON; otherwise show entire response
        if jq -r .error.message $response_body >/dev/null 2>&1; then
            jq -r .error.message $response_body >&2
        else
            cat $response_body >&2
        fi
        rc=1
    fi

    return $rc
}

_repo_name() {
    # Extract information about remote 'user/repository' from current repository
    git remote -v | grep -m1 '^origin' | awk '{ print $2; }' | awk -F '[:/]' '{OFS="/"; print $(NF-1),$NF; }' | sed 's/.git$//'
}

_branch_name() {
    git rev-parse --abbrev-ref HEAD
}

bb_pipeline_run() {
    # Start a pipeline run
    # Args: -n NAME         pipeline name

    local repo pipeline_name
    while getopts ":n:" option; do
        case $option in
            n )
                pipeline_name="${OPTARG}"
                ;;
            * )
                printf "Unknown option %s\n" "$option" >&2
                return 1
                ;;
        esac
    done

    repo="$(_repo_name)"
    echo "Requesting to run pipeline \"$pipeline_name\" on current branch in $repo..." >&2

    args=("$(_branch_name)" "$(git rev-parse HEAD)" "$pipeline_name")
    _pipeline_run "$repo" "${args[@]}"
}

_pipeline_run() {
    local repo branch revision pipeline_name url data rc
    repo="$1"
    branch="$2"
    revision="$3"
    pipeline_name="$4"

    url=https://api.bitbucket.org/2.0/repositories/$repo/pipelines/
    data="{
      \"target\": {
        \"commit\": {
          \"type\": \"commit\",
          \"hash\": \"$revision\"
        },
        \"selector\": { \"type\": \"custom\", \"pattern\": \"$pipeline_name\" },
        \"ref_type\": \"branch\",
        \"type\": \"pipeline_ref_target\",
        \"ref_name\": \"$branch\"
      }
    }"

    if _http_post "$url" -d "$data"; then
        rc=0
        printf "Started pipeline " >&2
        jq -r .uuid $response_body >&2

    else
        rc=1
    fi

    return $rc
}

bb_issue_list() {
    repo="$(_repo_name)"
    echo "Listing open/new issues in $repo..." >&2

    _list_all "$repo" issues
}

_list_all() {
    # Return all pages from the specified resource
    local rc url repo resource
    repo="$1"
    resource="$2"

    rc=0
    url=https://api.bitbucket.org/2.0/repositories/"$repo"/"$resource"

    while true; do
        if _http_get "$url"; then
            local state title id
            while IFS=  read -r; do
                state=$(echo "$REPLY" | jq -r .state)

                if [[ $state = new ]] || [[ ${state,,} = open ]]; then
                    title=$(echo "$REPLY" | jq -r .title)
                    id=$(echo "$REPLY" | jq -r .id)
                    printf '%s %s\n' "$id" "$title"
                fi
            done < <(jq -cr '.values[] | {title: .title, state: .state, id: .id}' $response_body)

            url=$(jq -r .next $response_body)
            if [[ "$url" = null ]]; then
                break
            fi

        else
            rc=1
            break
        fi
    done | sort -n -r

    return $rc
}

bb_pr_list() {
    repo="$(_repo_name)"
    echo "Listing open/new prs in $repo..." >&2

    _list_all "$repo" pullrequests
}

bb_pr_create() {
    # Create a pullrequest
    # Args: [-t TITLE]      pullrequest title (prompted for if not given)

    local repo title branch
    while getopts ":t:" option; do
        case $option in
            t )
                title="${OPTARG}"
                ;;
            * )
                printf "Unknown option %s\n" "$option" >&2
                return 1
                ;;
        esac
    done

    repo="$(_repo_name)"
    branch="$(_branch_name)"
    echo "Creating new pr from $branch into master in $repo..." >&2

    while [ -z "$title" ]; do
        read -r -p "Enter pr title: " title
    done

    ${EDITOR:-vim} /tmp/bibu-pr.md
    _pr_create "$repo" "$branch" "$title" /tmp/bibu-pr.md
}

_pr_create() {
    local repo branch title description_file url data rc
    repo="$1"
    branch="$2"
    title="$3"
    description_file="$4"

    url=https://api.bitbucket.org/2.0/repositories/$repo/pullrequests
    # Make newlines literal; escape double quotes
    data="{
      \"title\": \"$title\",
      \"description\": \"$(sed '$!s/$/\\r\\n\\r\\n/' "$description_file" | tr -d '\n' | sed 's/"/\\"/g')\",
      \"source\": {
        \"branch\": {
          \"name\": \"$branch\"
        }
      }
    }"

    if _http_post "$url" -d "$data"; then
        rc=0
        printf "Created pr #" >&2
        jq -r .id $response_body >&2

    else
        rc=1
    fi

    return $rc
}

bb_pipeline_list() {
    repo="$(_repo_name)"
    echo "Listing pipelines in $repo..." >&2

    _pipeline_list "$repo"
}

_pipeline_list() {
    local rc url repo
    repo="$1"

    url=https://api.bitbucket.org/2.0/repositories/$repo/pipelines/'?sort=-created_on'

    rc=0
    if _http_get "$url"; then
        local state

        while IFS=  read -r; do
            printf '%d ' "$(echo "$REPLY" | jq -r .build_number)"
            # Convert '2020-03-05T08:56:29.204Z' to '2020-03-05 08:56'
            printf '%s ' "$(echo "$REPLY" | jq -r .created_on | cut -d: -f1,2 | tr T ' ')"
            printf '%s ' "$(echo "$REPLY" | jq -r .creator.display_name | cut -d' ' -f1)"
            printf '%s ' "$(echo "$REPLY" | jq -r .target.ref_name)"

            state=$(echo "$REPLY" | jq -r .state.name)

            if [[ $state = IN_PROGRESS ]] || [[ $state = PENDING ]]; then
                printf '%s' "$state"
            elif [[ $state = COMPLETED ]]; then
                printf '%s' "$(echo "$REPLY" | jq -r .state.result.name)"
            fi
            printf '\n'
        done < <(jq -cr '.values[]' $response_body) | column -t

    else
        rc=1
    fi

    return $rc
}

inspect_bb_pipeline() {
    [[ $# -ne 1 ]] && { echo "Pipeline ID missing" >&2; return 1; }

    repo="$(_repo_name)"
    url="https://bitbucket.org/$repo/addon/pipelines/home#!/results/$1"

    echo "Opening $url..."
    xdg-open "$url"
}

bb_api() {
    # Run GET request of given REST API resource
    # Args: RESOURCE        resource string

    local resource url rc response
    resource="$1"
    url=https://api.bitbucket.org/2.0/repositories/"$(_repo_name)"/"$resource"

    rc=0
    if _http_get "$url"; then
        # Attempt to format as JSON
        if response=$(jq -r . "$response_body" 2>&1); then
            printf "%s\n" "$response"
        else
            cat "$response_body"
        fi
    else
        rc=1
    fi

    return $rc
}

_bb_refresh_access() {
    echo "Refreshing access token..." >&2

    local http_status rc

    rc=0
    http_status=$(curl -X POST -s \
        -w "%{http_code}" \
        -o $response_body \
        -u "$BITBUCKET_REST_API_AUTH" \
        https://bitbucket.org/site/oauth2/access_token \
        -d grant_type=refresh_token \
        -d refresh_token="$(jq -r .refresh_token $token_filepath)")

    if [ $http_status -lt 300 ]; then
        # Store tokens
        mv $response_body $token_filepath
    else
        echo "Error refreshing access ($http_status):" >&2
        jq -r . $response_body >&2
        rc=1
    fi

    return $rc
}

_bb_obtain_access() {
    # Obtain OAuth2 access token (only effective when not downloaded yet, i.e.
    # at first invocation of the command line interface)
    if [ -f "$token_filepath" ]; then
        return
    fi

    echo "Obtaining access token..." >&2
    local http_status rc

    http_status=$(curl -X POST -s \
        -w "%{http_code}" \
        -o $response_body \
        -u "$BITBUCKET_REST_API_AUTH" \
        https://bitbucket.org/site/oauth2/access_token \
        -d grant_type=client_credentials)

    if [ $http_status -lt 300 ]; then
        # Store tokens
        mv $response_body $token_filepath
        rc=0
    else
        echo "Error obtaining access ($http_status):" >&2
        jq -r . $response_body >&2
        rc=1
    fi

    return $rc
}

usage() {
    while IFS= read -r line; do
        printf '%s\n' "$line"
    done <<END_OF_HELP_TEXT
Usage: bibu COMMAND

A Bitbucket command line interface written in bash.
bibu operates on the repository of the current working directory, and derives
information from 'git-remote'.

Available commands:
    issue           Manage Bitbucket issues
    pipeline        Manage Bitbucket pipelines
    pr              Manage Bitbucket pullrequests
    api             Get resource via REST API

General options:
    --help          Display help message

Environment variables:
    BITBUCKET_REST_API_AUTH     Consumer OAuth of form key:secret
END_OF_HELP_TEXT
}

usage_issue() {
    while IFS= read -r line; do
        printf '%s\n' "$line"
    done <<END_OF_HELP_TEXT
Usage: bibu issue list
END_OF_HELP_TEXT
}

usage_pr() {
    while IFS= read -r line; do
        printf '%s\n' "$line"
    done <<END_OF_HELP_TEXT
Usage: bibu pr list
       bibu pr create [-t TITLE]
END_OF_HELP_TEXT
}

usage_pipeline() {
    while IFS= read -r line; do
        printf '%s\n' "$line"
    done <<END_OF_HELP_TEXT
Usage: bibu pipeline list
       bibu pipeline run [-n NAME]
END_OF_HELP_TEXT
}

usage_api() {
    while IFS= read -r line; do
        printf '%s\n' "$line"
    done <<END_OF_HELP_TEXT
Usage: bibu api RESOURCE
END_OF_HELP_TEXT
}

parse_command_line() {
    # Args:   [COMMAND [SUBCOMMAND [OPTIONS]]]
    # Stdout: function corresponding to command line parameters
    # Return: 0 if regular command
    #         1 if usage or invalid command
    local command subcommand function args
    args=()
    command="$1"; shift

    case "$command" in
        issue )
            subcommand="$1"; shift
            case "$subcommand" in
                list )
                    if [ $# -eq 0 ]; then
                        function=bb_issue_list
                    else
                        function=usage_issue
                    fi
                    ;;
                * )
                    function=usage_issue ;;
            esac
            ;;
        api )
            case "$1" in
                -h|--help|"" )
                    function=usage_api ;;
                * )
                    args+=("$1")
                    function=bb_api
                    ;;
            esac
            ;;
        pr )
            subcommand="$1"; shift
            case "$subcommand" in
                list )
                    if [ $# -eq 0 ]; then
                        function=bb_pr_list
                    else
                        function=usage_pr
                    fi
                    ;;
                create )
                    function=bb_pr_create
                    while getopts ":t-:" option; do
                        case $option in
                            t )
                                args+=(-t "${!OPTIND}")
                                ((OPTIND++))
                                ;;
                            * )
                                function=usage_pr ;;
                        esac
                    done
                    shift $((OPTIND-1))
                    ;;
                * )
                    function=usage_pr ;;
            esac
            ;;
        pipeline )
            subcommand="$1"; shift
            case "$subcommand" in
                list )
                    if [ $# -eq 0 ]; then
                        function=bb_pipeline_list
                    else
                        function=usage_pipeline
                    fi
                    ;;
                run )
                    function=bb_pipeline_run
                    while getopts ":n-:" option; do
                        case $option in
                            n )
                                args+=(-n "${!OPTIND}")
                                ((OPTIND++))
                                ;;
                            * )
                                function=usage_pipeline ;;
                        esac
                    done
                    shift $((OPTIND-1))
                    ;;
                * )
                    function=usage_pipeline ;;
            esac
            ;;
        * )
            function=usage ;;
    esac

    echo $function "${args[@]}"

    [[ "$function" = "usage"* ]] && return 1 || return 0
}

main() {
    # Check dependencies
    local deps_ready
    deps_ready=true
    for dep in jq curl; do
        if ! command -v $dep >/dev/null 2>&1; then
            printf "Can't find dependency: %s\n" $dep
            deps_ready=false
        fi
    done
    $deps_ready || return 1

    # Check for environment variable
    if [ -z "$BITBUCKET_REST_API_AUTH" ]; then
        printf "Obtain OAuth consumer key and secret from your Bitbucket profile\n" >&2
        printf "settings, and store them in %s.\n" "\$BITBUCKET_REST_API_AUTH" >&2
        return 1
    fi

    # Parse command line and run according functionality
    local function rc
    function="$(parse_command_line "$@")"
    rc=$?

    if [[ "$function" != "usage"* ]]; then
        _bb_obtain_access
    fi

    $function
    return $rc
}
