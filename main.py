import datetime
import json
import os
import github


def verified_label_prs(pull, commit):
    label = "Verified"
    is_verified = False
    labels = get_labels(pull)
    last_commit = list(pull.get_commits())[-1]
    last_commit_time = datetime.datetime.strptime(last_commit.stats.last_modified, '%a, %d %b %Y %H:%M:%S %Z')

    verified = [ic for ic in pull.get_issue_comments() if "/verified" in ic.body]
    if verified:
        for _verified in verified:
            is_verified = last_commit_time < _verified.created_at
            if is_verified:
                break

    if is_verified:
        if label not in labels:
            print(f"Adding {label} to {pull.title}")
            pull.add_to_labels(label)

    else:
        if label in labels:
            print(f"Removing {label} from {pull.title}")
            pull.remove_from_labels(label)


def get_labels(pull):
    return [label.name for label in pull.get_labels()]


def add_reviewers(pull, commit):
    # reviewers = ["myakove", "rnetser", "AdiZav"]
    reviewers = ["myakove"]
    author = [commit.author.login]
    current_reviewers_requests = [reviewer.login for reviewer in pull.get_review_requests()[0]]
    current_reviewers = set([reviewer.user.login for reviewer in pull.get_reviews()])
    for reviewer in reviewers:
        if reviewer not in (current_reviewers_requests or current_reviewers or author):
            print(f"Requesting review from {reviewer} for {pull.title}")
            pull.create_review_request([reviewer])


def size_label_prs(pull):
    label = None
    labels = get_labels(pull=pull)
    additions = pull.raw_data["additions"]
    if additions < 20:
        label = "Size/XS"

    elif additions < 50:
        label = "Size/S"

    elif additions < 100:
        label = "Size/M"

    elif additions < 300:
        label = "Size/L"

    elif additions < 500:
        label = "Size/XL"

    if label in labels:
        return

    else:
        print(f"Labeling {pull.title}: {label}")
        [pull.remove_from_labels(lb) for lb in labels if lb.startswith("Size/")]
        pull.add_to_labels(label)


if __name__ == "__main__":
    token = os.environ['INPUT_TOKEN']
    event_type = os.environ["GITHUB_EVENT_NAME"]
    print(event_type)
    print(os.environ.get("GITHUB_EVENT_PATH"))
    print(os.environ.get("GITHUB_SHA"))
    print(os.environ.get("GITHUB_REF"))
    with open(os.environ.get("GITHUB_EVENT_PATH"), "r") as fd:
        data = json.load(fd)

    print(data)
    github = github.Github(token)
    repo = github.get_repo(os.environ['GITHUB_REPOSITORY'])
    commit = repo.get_commit(os.environ.get("GITHUB_SHA"))
    pull = repo.get_pull(data["number"])
    size_label_prs(pull=pull)
    add_reviewers(pull=pull, commit=commit)


