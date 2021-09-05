from src.constants import (
    BLOCK_MERGE_VERIFY_CONTEXT,
    LABEL_APPROVE,
    LABEL_VERIFIED,
    NEEDS_MAINTAINERS_APPROVE,
    READY_FOR_MERGE,
    STATE_PENDING,
    STATUS_DESCRIPTION_MISSING_MAINTAINERS_APPROVAL,
    STATUS_DESCRIPTION_MISSING_VERIFIED,
)
from src.utils import remove_label


def remove_merge_checks(pull):
    last_commit = list(pull.get_commits())[-1]
    remove_label(pull=pull, label=LABEL_VERIFIED)
    remove_label(pull=pull, label=LABEL_APPROVE)
    remove_label(pull=pull, label=READY_FOR_MERGE)
    last_commit.create_status(
        state=STATE_PENDING,
        description=STATUS_DESCRIPTION_MISSING_VERIFIED,
        context=BLOCK_MERGE_VERIFY_CONTEXT,
    )
    last_commit.create_status(
        state=STATE_PENDING,
        description=STATUS_DESCRIPTION_MISSING_MAINTAINERS_APPROVAL,
        context=NEEDS_MAINTAINERS_APPROVE,
    )
