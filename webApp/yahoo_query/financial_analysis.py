import yfinance as yf


def financeAnalisis(symbol):
    info_tags = [
        "symbol",
        "shortName",
        "debtToEquity",
        "heldPercentInsiders",
        "currentPrice",
        "targetMeanPrice",
        "trailingPE",
        "forwardPE",
        "trailingEps",
        "forwardEps",
        "returnOnAssets",
        "returnOnEquity",
        "profitMargins",
    ]
    row_with_tag_data = []
    existant_info_tags = {}
    ticker = yf.Ticker(symbol)
    count = 0
    for info in info_tags:
        try:
            existant_info_tags[info] = ticker.info[info]
        except:
            if info == "symbol":
                existant_info_tags[info] = symbol
            else:
                existant_info_tags[info] = -404
    for key in existant_info_tags:
        if (
            (key == "heldPercentInsiders" and existant_info_tags[key] != -404)
            or (key == "returnOnAssets" and existant_info_tags[key] != -404)
            or (key == "returnOnEquity" and existant_info_tags[key] != -404)
            or (key == "profitMargins" and existant_info_tags[key] != -404)
        ):
            row_with_tag_data.append(existant_info_tags[key] * 100)
        elif key == "debtToEquity" and existant_info_tags[key] != -404:
            row_with_tag_data.append(existant_info_tags[key] / 100)
        elif key == "targetMeanPrice" and existant_info_tags[key] != -404:
            row_with_tag_data.append(existant_info_tags[key])
            row_with_tag_data.append(
                100
                * ((existant_info_tags[key] / existant_info_tags["currentPrice"]) - 1)
            )
        elif key == "targetMeanPrice" and existant_info_tags[key] == -404:
            row_with_tag_data.append(-404)
            row_with_tag_data.append(-404)
        elif existant_info_tags[key] == -404:
            row_with_tag_data.append(-404)
        else:
            row_with_tag_data.append(existant_info_tags[key])

    if (
        existant_info_tags["forwardPE"] != -404
        and existant_info_tags["trailingPE"] != -404
        and existant_info_tags["forwardEps"] != -404
        and existant_info_tags["trailingEps"] != -404
        and existant_info_tags["debtToEquity"] != -404
        and existant_info_tags["heldPercentInsiders"] != -404
        and existant_info_tags["targetMeanPrice"] != -404
        and existant_info_tags["returnOnEquity"] != -404
        and existant_info_tags["profitMargins"] != -404
    ):
        x = 0
        y = 0

        if existant_info_tags["forwardPE"] < existant_info_tags["trailingPE"]:
            count += 1
            x = 0.04
        if existant_info_tags["forwardEps"] > existant_info_tags["trailingEps"]:
            count += 1
            y = 0.03
        row_with_tag_data.append(
            0.08 * 20 * (existant_info_tags["debtToEquity"] / 100)
            + 0.04 * 2 * existant_info_tags["heldPercentInsiders"] * 100
            + 0.35
            * 100
            * (
                existant_info_tags["targetMeanPrice"]
                / existant_info_tags["currentPrice"]
                - 1
            )
            + 0.04 * 2.5 * existant_info_tags["trailingPE"]
            + x
            + y
            + 0.02 * 3.3 * existant_info_tags["returnOnAssets"] * 100
            + 0.2 * 0.66 * existant_info_tags["returnOnEquity"] * 100
            + 0.2 * 2.5 * existant_info_tags["profitMargins"] * 100
        )
    else:
        row_with_tag_data.append(-404)
    if (
        existant_info_tags["debtToEquity"] < 1
        and existant_info_tags["debtToEquity"] != -404
    ):
        count += 1
    if (
        existant_info_tags["heldPercentInsiders"] > 0.05
        and existant_info_tags["heldPercentInsiders"] != -404
    ):
        count += 1
    if (
        100
        * (
            (existant_info_tags["targetMeanPrice"] / existant_info_tags["currentPrice"])
            - 1
        )
        > 50
        and existant_info_tags["targetMeanPrice"] != -404
        and existant_info_tags["currentPrice"] != -404
    ):
        count += 1
    if (
        existant_info_tags["returnOnAssets"] > 0.15
        and existant_info_tags["returnOnAssets"] != -404
    ):
        count += 1
    if (
        existant_info_tags["returnOnEquity"] > 0.2
        and existant_info_tags["returnOnEquity"] != -404
    ):
        count += 1
    if (
        existant_info_tags["profitMargins"] > 0.25
        and existant_info_tags["profitMargins"] != -404
    ):
        count += 1
    row_with_tag_data.append(count)

    for i in range(1, len(row_with_tag_data)):
        if type(row_with_tag_data[i]) == float:
            row_with_tag_data[i] = round(row_with_tag_data[i], 3)
    return row_with_tag_data


if __name__ == "__main__":
    tags = [
        "GOOGL",
        "META",
        "APR",
        "MEDP",
        "SFM",
        "FRAGUAB",
        "AEP",
        "SDI",
        "NA9",
        "ULTA",
        "METC",
    ]

    for tag in tags:
        print(financeAnalisis(tag))
