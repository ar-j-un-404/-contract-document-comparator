def print_report(results):
    print("\n")
    print("=" * 60)
    print("CONTRACT COMPARISON REPORT")
    print("=" * 60)

    for i, result in enumerate(results, start=1):
        print()
        print("-" * 60)
        print(f"Change {i}")
        print("-" * 60)

        print("Status:", result["status"])
        print("Risk:", result["risk"])

        if result["old_clause"]:
            print(
                "Old Clause:",
                result["old_clause"]["title"]
            )

        if result["new_clause"]:
            print(
                "New Clause:",
                result["new_clause"]["title"]
            )

        if result["similarity"]:
            print(
                "Similarity:",
                round(
                    result["similarity"] * 100,
                    2
                ),
                "%"
            )

        if result["field_changes"]:
            print("Important Changes:")

            for field, values in result["field_changes"].items():
                print(
                    f"  {field}: "
                    f"{values['old']} -> {values['new']}"
                )

        if "explanation" in result:
            print()
            print("AI Explanation:")
            print(result["explanation"])

    print()
    print("=" * 60)