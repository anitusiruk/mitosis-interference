from collections import defaultdict

import numpy as np
from datasets import load_dataset


DOMAINS = {
    "A": "home",
    "B": "apparel",
    "C": "drugstore",
}


def sentiment_label(stars):
    stars = int(stars)

    if stars <= 2:
        return 0

    if stars >= 4:
        return 1

    return None


def collect_examples(ds):
    out = defaultdict(
        lambda: {
            0: [],
            1: [],
        }
    )

    wanted = set(
        DOMAINS.values()
    )

    for i, row in enumerate(ds):
        domain = row["product_category"]

        if domain not in wanted:
            continue

        label = sentiment_label(
            row["stars"]
        )

        if label is None:
            continue

        text = row["review_body"]

        if not text:
            continue

        out[domain][label].append({
            "id": int(i),
            "text": str(text),
            "label": int(label),
        })

    return out


def make_segment(
    neg_rows,
    pos_rows,
    batch_size,
    rng,
    concept,
    occurrence,
):
    rows = (
        list(neg_rows)
        + list(pos_rows)
    )

    order = np.arange(
        len(rows)
    )

    rng.shuffle(order)

    rows = [
        rows[int(i)]
        for i in order
    ]

    batches = []

    for start in range(
        0,
        len(rows),
        batch_size,
    ):
        chunk = rows[
            start:
            start + batch_size
        ]

        if not chunk:
            continue

        batches.append({
            # Evaluation metadata only.
            # Never supplied to controller.
            "concept": concept,
            "occurrence": occurrence,
            "domain":
                DOMAINS[concept],

            "texts": [
                x["text"]
                for x in chunk
            ],

            "labels": [
                x["label"]
                for x in chunk
            ],

            "source_ids": [
                x["id"]
                for x in chunk
            ],
        })

    return batches


def build_domain_recurrence(
    seed,
    batch_size=16,
    train_per_class=128,
    eval_per_class=64,
):
    # Explicitly instantiate only train/validation.
    train_ds = load_dataset(
        "goosmanlei/amazon_reviews_multi",
        "en",
        split="train",
    )

    val_ds = load_dataset(
        "goosmanlei/amazon_reviews_multi",
        "en",
        split="validation",
    )

    train = collect_examples(
        train_ds
    )

    val = collect_examples(
        val_ds
    )

    rng = np.random.default_rng(
        seed
    )

    selections = {}

    for concept, domain in (
        DOMAINS.items()
    ):
        selections[concept] = {}

        for label in [0, 1]:
            ids = np.arange(
                len(train[domain][label])
            )

            rng.shuffle(ids)

            need = (
                2 * train_per_class
                if concept in {"A", "B"}
                else train_per_class
            )

            if len(ids) < need:
                raise RuntimeError(
                    f"{domain} label {label}: "
                    f"need {need}, "
                    f"have {len(ids)}"
                )

            selected = [
                train[domain][label][
                    int(i)
                ]
                for i in ids[:need]
            ]

            if concept in {"A", "B"}:
                selections[concept][
                    (1, label)
                ] = selected[
                    :train_per_class
                ]

                selections[concept][
                    (2, label)
                ] = selected[
                    train_per_class:
                    2 * train_per_class
                ]
            else:
                selections[concept][
                    (1, label)
                ] = selected[
                    :train_per_class
                ]

    schedule = [
        ("A", 1),
        ("B", 1),
        ("A", 2),
        ("C", 1),
        ("B", 2),
    ]

    stream = []
    boundaries = []

    for concept, occurrence in (
        schedule
    ):
        neg = selections[
            concept
        ][
            (occurrence, 0)
        ]

        pos = selections[
            concept
        ][
            (occurrence, 1)
        ]

        segment = make_segment(
            neg_rows=neg,
            pos_rows=pos,
            batch_size=batch_size,
            rng=rng,
            concept=concept,
            occurrence=occurrence,
        )

        stream.extend(segment)

        if len(stream) < 5 * (
            2 * train_per_class
            // batch_size
        ):
            boundaries.append(
                len(stream) + 1
            )

    # Fixed, balanced validation sets.
    eval_sets = {}

    eval_rng = (
        np.random.default_rng(
            424242
        )
    )

    for concept, domain in (
        DOMAINS.items()
    ):
        rows = []

        for label in [0, 1]:
            ids = np.arange(
                len(val[domain][label])
            )

            eval_rng.shuffle(ids)

            if len(ids) < eval_per_class:
                raise RuntimeError(
                    f"validation {domain} "
                    f"label {label}: "
                    f"need {eval_per_class}, "
                    f"have {len(ids)}"
                )

            rows.extend([
                val[domain][label][
                    int(i)
                ]
                for i in ids[
                    :eval_per_class
                ]
            ])

        eval_sets[concept] = {
            "domain": domain,
            "texts": [
                x["text"]
                for x in rows
            ],
            "labels": [
                x["label"]
                for x in rows
            ],
            "source_ids": [
                x["id"]
                for x in rows
            ],
        }

    return (
        stream,
        boundaries,
        eval_sets,
    )
