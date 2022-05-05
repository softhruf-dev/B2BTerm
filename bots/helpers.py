import io
import logging
import os
import re
import uuid
from typing import Any, Dict, List

import disnake
import financedatabase as fd
import natsort
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from kaleido.scopes.plotly import PlotlyScope
from numpy.core.fromnumeric import transpose
from PIL import Image
from plotly.offline import plot

from bots import imps
from bots.groupme.groupme_helpers import send_image, send_message

# pylint: disable=W0613
logger = logging.getLogger(__name__)

presets_custom = [
    "potential_reversals",
    "golden_cross_penny",
    "rosenwald_gtfo",
    "golden_cross",
    "bull_runs_over_10pct",
    "recent_growth_and_support",
    "heavy_inst_ins",
    "short_squeeze_scan",
    "under_15dol_stocks",
    "top_performers_healthcare",
    "oversold_under_3dol",
    "value_stocks",
    "cheap_dividend",
    "death_cross",
    "top_performers_tech",
    "unusual_volume",
    "cheap_oversold",
    "undervalue",
    "high_vol_and_low_debt",
    "simplistic_momentum_scanner_under_7dol",
    "5pct_above_low",
    "growth_stocks",
    "cheap_bottom_dividend",
    "analyst_strong_buy",
    "oversold",
    "rosenwald",
    "weak_support_and_top_performers",
    "channel_up_and_low_debt_and_sma_50and200",
    "template",
    "modified_neff",
    "buffett_like",
    "oversold_under_5dol",
    "sexy_year",
    "news_scanner",
    "top_performers_all",
    "stocks_strong_support_levels",
    "continued_momentum_scan",
    "modified_dreman",
    "break_out_stocks",
]
signals = [
    "top_gainers",
    "top_losers",
    "new_high",
    "new_low",
    "most_volatile",
    "most_active",
    "unusual_volume",
    "overbought",
    "oversold",
    "downgrades",
    "upgrades",
    "earnings_before",
    "earnings_after",
    "recent_insider_buying",
    "recent_insider_selling",
    "major_news",
    "horizontal_sr",
    "tl_resistance",
    "tl_support",
    "wedge_up",
    "wedge_down",
    "wedge",
    "triangle_ascending",
    "triangle_descending",
    "channel_up",
    "channel_down",
    "channel",
    "double_top",
    "double_bottom",
    "multiple_top",
    "multiple_bottom",
    "head_shoulders",
    "head_shoulders_inverse",
]

metric_yf_keys = {
    "Return On Assets": ("financialData", "returnOnAssets"),
    "Return On Equity": ("financialData", "returnOnEquity"),
    "Current Ratio": ("financialData", "currentRatio"),
    "Quick Ratio": ("financialData", "quickRatio"),
    "Debt To Equity": ("financialData", "debtToEquity"),
    "Total Cash": ("financialData", "totalCash"),
    "Total Cash Per Share": ("financialData", "totalCashPerShare"),
    "Total Revenue": ("financialData", "totalRevenue"),
    "Revenue Per Share": ("financialData", "revenuePerShare"),
    "Revenue Growth": ("financialData", "revenueGrowth"),
    "Earnings Growth": ("financialData", "earningsGrowth"),
    "Profit Margins": ("financialData", "profitMargins"),
    "Gross Profits": ("financialData", "grossProfits"),
    "Gross Margins": ("financialData", "grossMargins"),
    "Operating Cashflow": ("financialData", "operatingCashflow"),
    "Operating Margins": ("financialData", "operatingMargins"),
    "Free Cashflow": ("financialData", "freeCashflow"),
    "Total Debt": ("financialData", "totalDebt"),
    "Earnings Before Interest, Taxes, Depreciation and Amortization": (
        "financialData",
        "ebitda",
    ),
    "EBITDA Margins": ("financialData", "ebitdaMargins"),
    "Recommendation Mean": ("financialData", "recommendationMean"),
    "Market Cap": ("price", "marketCap"),
    "Full Time Employees": ("summaryProfile", "fullTimeEmployees"),
    "Enterprise To Revenue": ("defaultKeyStatistics", "enterpriseToRevenue"),
    "Book Value": ("defaultKeyStatistics", "bookValue"),
    "Shares Short": ("defaultKeyStatistics", "sharesShort"),
    "Price To Book": ("defaultKeyStatistics", "priceToBook"),
    "Beta": ("defaultKeyStatistics", "beta"),
    "Float Shares": ("defaultKeyStatistics", "floatShares"),
    "Short Ratio": ("defaultKeyStatistics", "shortRatio"),
    "Peg Ratio": ("defaultKeyStatistics", "pegRatio"),
    "Enterprise Value": ("defaultKeyStatistics", "enterpriseValue"),
    "Forward PE": ("defaultKeyStatistics", "forwardPE"),
}

# kaleido Scope to handle all plots image converting
scope = PlotlyScope(
    plotlyjs=imps.bots_path.joinpath("interactive/plotly.js"),
)


def load(ticker, start_date):
    df_stock_candidate = yf.download(ticker, start=start_date, progress=False)
    df_stock_candidate.index.name = "date"
    return df_stock_candidate


def quote(ticker):
    ticker = yf.Ticker(ticker)
    quote_df = pd.DataFrame(
        [
            {
                "Symbol": ticker.info["symbol"],
                "Name": ticker.info["shortName"],
                "Price": ticker.info["regularMarketPrice"],
                "Open": ticker.info["regularMarketOpen"],
                "High": ticker.info["dayHigh"],
                "Low": ticker.info["dayLow"],
                "Previous Close": ticker.info["previousClose"],
                "Volume": ticker.info["volume"],
                "52 Week High": ticker.info["fiftyTwoWeekHigh"],
                "52 Week Low": ticker.info["fiftyTwoWeekLow"],
            }
        ]
    )
    quote_df["Change"] = quote_df["Price"] - quote_df["Previous Close"]
    quote_df["Change %"] = quote_df.apply(
        lambda x: f'{((x["Change"] / x["Previous Close"]) * 100):.2f}%',
        axis="columns",
    )
    for c in [
        "Price",
        "Open",
        "High",
        "Low",
        "Previous Close",
        "52 Week High",
        "52 Week Low",
        "Change",
    ]:
        quote_df[c] = quote_df[c].apply(lambda x: f"{x:.2f}")
    quote_df["Volume"] = quote_df["Volume"].apply(lambda x: f"{x:,}")

    quote_df = quote_df.set_index("Symbol")
    quote_data = transpose(quote_df)
    return quote_data


def autocrop_image(image: Any, border=0) -> Any:
    """Crop empty space from PIL image

    Parameters
    ----------
    image : Image
        PIL image to crop
    border : int, optional
        scale border outwards, by default 0

    Returns
    -------
    Image
        Cropped image
    """
    bbox = image.getbbox()
    image = image.crop(bbox)
    (width, height) = image.size
    width += border * 2
    height += border * 2
    cropped_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    cropped_image.paste(image, (border, border))
    return cropped_image


conversion_mapping = {
    "K": 1_000,
    "M": 1_000_000,
}

all_units = "|".join(conversion_mapping.keys())
float_re = natsort.numeric_regex_chooser(natsort.ns.FLOAT | natsort.ns.SIGNED)
unit_finder = re.compile(rf"({float_re})\s*({all_units})", re.IGNORECASE)


def unit_replacer(matchobj):
    """
    Given a regex match object, return a replacement string where units are modified
    """
    number = matchobj.group(1)
    unit = matchobj.group(2)
    new_number = float(number) * conversion_mapping[unit]
    return f"{new_number}"


def uuid_get() -> str:
    """Returns a UUID

    Returns
    -------
    str
        UUID Ex. e48c4851a42711ec8e11fb53fa4c20e5
    """
    rand = str(uuid.uuid1()).replace("-", "")
    return rand


def country_autocomp(inter, country: str):
    data = fd.show_options("equities", "countries")
    clow = country.lower()
    return [country for country in data if country.lower().startswith(clow)][:24]


def industry_autocomp(inter, industry: str):
    data = fd.show_options("equities", "industries")
    if not industry:
        industry = "a"
    ilow = industry.lower()
    return [industry for industry in data if industry.lower().startswith(ilow)][:24]


def metric_autocomp(inter, metric: str):
    data: dict = metric_yf_keys
    if not metric:
        data = list(data.keys())  # type: ignore
        return data[:24]
    mlow = metric.lower()
    return [metric for metric, _ in data.items() if metric.lower().startswith(mlow)][
        :24
    ]


def ticker_autocomp(inter, ticker: str):
    if not ticker:
        return ["Start Typing", "for a", "stock ticker"]
    print(f"ticker_autocomp [ticker]: {ticker}")
    tlow = ticker.lower()
    col_list = ["Name"]
    file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "files",
        "tickers.csv",
    )
    df = pd.read_csv(file, usecols=col_list)
    df = df["Name"]
    return [ticker for ticker in df if ticker.lower().startswith(tlow)][:24]


def expiry_autocomp(inter, ticker: str):
    data = inter.filled_options["ticker"]
    yf_ticker = yf.Ticker(data)
    dates = list(yf_ticker.options)
    return dates[:24]


def presets_custom_autocomp(inter, preset: str):
    df = presets_custom
    if not preset:
        return df[:24]
    plow = preset.lower()
    print(f"preset_custom_autocomp [preset]: {preset}")
    return [preset for preset in df if preset.lower().startswith(plow)][:24]


def signals_autocomp(inter, signal: str):
    df = signals
    if not signal:
        return df[:24]
    print(f"signal_autocomp [signal]: {signal}")
    slow = signal.lower()
    return [signal for signal in df if signal.lower().startswith(slow)][:24]


def in_decreasing_color_list(df_column: pd.DataFrame.columns) -> List[str]:
    """Makes a colorlist for increase/decrease if value in df_column contains "-"

    Parameters
    ----------
    df_column : pd.DataFrame.columns
        Dataframe column to create colorlist.

    Returns
    -------
    List[str]
        List of colors for df_column
    """
    colorlist = [
        imps.PLT_CANDLE_DECREASING if boolv else imps.PLT_CANDLE_INCREASING
        for boolv in df_column.str.contains("-")
    ]
    return colorlist


def chart_volume_scaling(
    df_column: pd.DataFrame.columns, range_x: int = 5
) -> Dict[str, list]:
    """Takes df_column and returns volume_ticks, tickvals for chart volume scaling

    Parameters
    ----------
    df_column : pd.DataFrame.columns
        Dataframe column
    range_x : int, optional
        Number to multiply volume, by default 5
    Returns
    -------
    Dict[str, list]
        {"range": volume_range, "ticks": tickvals}
    """
    df_column = df_column.apply(lambda x: f"{x:.1f}")
    df_column = pd.to_numeric(df_column.astype(float))
    volume_ticks = (df_column.values.max()).astype(int)
    round_digits = -3
    first_val = round(volume_ticks * 0.20, round_digits)
    if len(str(volume_ticks)) > 5:
        round_digits = -4
        first_val = round(volume_ticks * 0.20, round_digits)
    if len(str(volume_ticks)) > 6:
        round_digits = -5
        first_val = round(volume_ticks * 0.20, round_digits)
    if len(str(volume_ticks)) > 7:
        round_digits = -6
        first_val = round(volume_ticks * 0.20, round_digits)
    if len(str(volume_ticks)) > 8:
        round_digits = -8
        first_val = round(volume_ticks * 0.20, round_digits)
    if len(str(volume_ticks)) > 9:
        round_digits = -9
        first_val = round(volume_ticks * 0.20, round_digits)
    tickvals = [
        first_val * 1,
        first_val * 2,
        first_val * 3,
        first_val * 4,
        first_val * 5,
    ]
    volume_range = [0, (volume_ticks * range_x)]
    return {"range": volume_range, "ticks": tickvals}


def inter_chart(fig: go.Figure, filename: str, **data) -> str:
    """Takes plotly chart object and saves as a html file for interactive charts

    Parameters
    ----------
    fig : go.Figure
        go.Figure chart object
    filename : str
        Name to save html as
    **kawrgs:
        config: dict = plotly config Ex. dict(scrollZoom=True, displayModeBar=False)
        callback: bool = enable js_callback for clickable news
    Returns
    -------
    str
        Link for interactive charts Ex. "[Interactive]({imps.INTERACTIVE_URL}/{filename})"
    """
    filename = f"{filename.replace('.png', '')}_{uuid_get()}.html"
    if "config" not in data:
        config = dict(scrollZoom=True, displayModeBar=False)
    plot_div = plot(fig, output_type="div", include_plotlyjs="plotly.js", config=config)
    if data["callback"]:
        res = re.search('<div id="([^"]*)"', plot_div)
        if res is not None:
            res = res.groups()[0]
            div_id = res

        js_callback = f"""
        <script>
        var plot_element = document.getElementById("{div_id}");
        plot_element.on('plotly_click', function(data){{
            console.log(data);
            var point = data.points[0];
            if (point) {{
                console.log(point.customdata[1]);
                window.open(point.customdata[1]);
            }}
        }})
        </script>
        """

        # Build HTML string
        html_str = f"""
        <html>
        <body style="background-color:#111111;">
        <body>
        {plot_div}
        {js_callback}
        </body>
        </html>
        """
    else:
        # Build HTML string
        html_str = f"""
        <html>
        <body style="background-color:#111111;">
        <body>
        {plot_div}
        </body>
        </html>
        """

    # Write out HTML file
    with open(f"{imps.INTERACTIVE_DIR.joinpath(filename)}", "w") as f:
        f.write(html_str)
    plt_link = f"[Interactive]({imps.INTERACTIVE_URL}/{filename})"
    return plt_link


def save_image(filename: str, fig: go.Figure = None, bytesIO: io.BytesIO = None) -> str:
    """Takes go.Figure or io.BytesIO object, adds uuid to filename, autocrops, and saves

    Parameters
    ----------
    filename : str
        Name to save image as
    fig : go.Figure, optional
        Table object to autocrop and save, by default None
    bytesIO : io.BytesIO, optional
        BystesIO object to autocrop and save, by default None

    Returns
    -------
    str
        filename with UUID added to use for bot processing

    Raises
    ------
    Exception
        Function requires a go.Figure or BytesIO object
    """
    imagefile = f"{filename.replace('.png', '')}_{uuid_get()}.png"
    filesave = imps.IMG_DIR.joinpath(imagefile)
    if fig:
        # Transform Fig into PNG with Running Scope. Returns image bytes
        fig = scope.transform(fig, scale=3, format="png")
        imgbytes = io.BytesIO(fig)
    elif bytesIO:
        imgbytes = bytesIO
    else:
        raise Exception("Function requires a go.Figure or io.BytesIO object")

    image = Image.open(imgbytes)
    image = autocrop_image(image, 0)
    imgbytes.seek(0)
    image.save(filesave, "PNG", quality=100)
    image.close()

    return imagefile


def image_border(
    filename: str, fig: go.Figure = None, base64: io.BytesIO = None, **kwargs
) -> str:
    """Takes fig, base64, or already saved image and adds border to it

    Parameters
    ----------
    filename : str
        Name to save image as. If no fig or base64, will try to find
        an image with this name to open.
    fig : go.Figure, optional
        Table object to add border to, by default None
    base64 : io.BytesIO, optional
        BystesIO object to add border to, by default None
    Returns
    -------
    str
        filename with UUID added to use for bot processing
    """
    imagefile = f"{filename.replace('.png', '')}_{uuid_get()}.png"
    filesave = imps.IMG_DIR.joinpath(imagefile)
    im_bgbytes = io.BytesIO()
    if fig:
        # Transform Fig into PNG with Running Scope. Returns image bytes
        fig = scope.transform(fig, scale=5, format="png")
        imgbytes = io.BytesIO(fig)
        img = Image.open(imgbytes)
    elif base64:
        img = Image.open(base64)
    else:
        img = Image.open(filename)

    im_bg = Image.open(imps.IMG_BG)
    im_bg = im_bg.resize((4200, 2600), resample=Image.Resampling.LANCZOS)  # type: ignore

    w = img.width + 520
    h = img.height

    # Paste fig onto background img and autocrop background
    img = img.resize((w, h), resample=Image.Resampling.LANCZOS)  # type: ignore
    x1 = int(0.5 * im_bg.size[0]) - int(0.5 * img.size[0])
    y1 = int(0.5 * im_bg.size[1]) - int(0.5 * img.size[1])
    x2 = int(0.5 * im_bg.size[0]) + int(0.5 * img.size[0])
    y2 = int(0.5 * im_bg.size[1]) + int(0.5 * img.size[1])
    img = img.convert("RGB")
    im_bg.paste(img, box=(x1 + 5, y1 + 10, x2 + 5, y2 + 10))
    img.close()
    im_bg.save(im_bgbytes, "PNG", quality=100)
    im_bg.close()
    im_bgbytes.seek(0)
    image = Image.open(im_bgbytes)
    image = imps.autocrop_image(image, 0)
    image = image.resize((1800, 1200), resample=Image.Resampling.LANCZOS)  # type: ignore
    image.save(filesave, "PNG")
    image.close()
    return imagefile


def multi_image(filename: str, **kwargs) -> str:
    """Uploads to an image host and returns image url.

    Parameters
    ----------
    filename : str
        Image filename

    Returns
    -------
    str
        Image url
    """
    if imps.IMAGES_URL or not imps.IMG_HOST_ACTIVE:
        image_link = str(imps.IMAGES_URL) + str(filename)
    else:
        imagefile_save = imps.IMG_DIR.joinpath(filename)
        uploaded_image = imps.openbb_imgur.upload_image(
            imagefile_save, title="something"
        )
        image_link = uploaded_image.link
        os.remove(imagefile_save)

    return image_link


class ShowView:
    async def run_discord(self, func, inter, *args, **kwargs):
        data = func(*args, **kwargs)

        if "view" in data:
            await inter.send(
                embed=data["embed"][0],
                view=data["view"](data["embed"], data["choices"]),
            )

        else:
            title = data.get("title", "")
            embed = disnake.Embed(
                title=title, colour=imps.COLOR, description=data.get("description", "")
            )
            embed.set_author(
                name=imps.AUTHOR_NAME,
                icon_url=imps.AUTHOR_ICON_URL,
            )
            if "imagefile" in data:
                filename = data["imagefile"]
                imagefile = imps.IMG_DIR.joinpath(filename)
                image = disnake.File(imagefile, filename=filename)
                embed.set_image(url=f"attachment://{filename}")
                await inter.send(embed=embed, file=image)
                image.close()
                os.remove(imagefile)
            else:
                await inter.send(embed=embed)

    async def discord(self, func, inter, name, *args, **kwargs):
        await inter.response.defer()
        logger.info(name)
        if os.environ.get("DEBUG_MODE") == "true":
            await self.run_discord(func, inter, *args, **kwargs)
        else:
            try:
                await self.run_discord(func, inter, *args, **kwargs)
            except Exception as e:
                embed = disnake.Embed(
                    title=name,
                    colour=imps.COLOR,
                    description=e,
                )
                embed.set_author(
                    name=imps.AUTHOR_NAME,
                    icon_url=imps.AUTHOR_ICON_URL,
                )

                await inter.send(embed=embed, delete_after=30.0)

    def groupme(self, func, group_id, name, *args, **kwargs):
        data = func(*args, **kwargs)
        if "imagefile" in data:
            imagefile = imps.IMG_DIR.joinpath(data["imagefile"])
            send_image(imagefile, group_id, data.get("description", ""))
            os.remove(imagefile)
        elif "embeds_img" in data:
            imagefiles = data["images_list"]
            for img in imagefiles:
                imagefile = imps.IMG_DIR.joinpath(img)
                send_image(imagefile, group_id, data.get("description", ""))
                os.remove(imagefile)
        elif "description" in data:
            title = data.get("title", "")
            # TODO: Allow navigation through pages
            description = data.get("description")
            if isinstance(description, List):
                clean_desc = description[0].replace("Page ", "")
            else:
                clean_desc = description.replace("Page ", "")
            message = f"{title}\n{clean_desc}"
            send_message(message, group_id)

    def slack(self, func, channel_id, user_id, client, *args, **kwargs):
        data = func(*args, **kwargs)
        if "imagefile" in data:
            title = data.get("title", "")
            description = (
                data.get("description", "")
                .replace("[Interactive](", "")
                .replace(".html)", ".html\n\n")
            )
            message = f"{title}\n{description}"
            imagefile = imps.IMG_DIR.joinpath(data["imagefile"]).__str__()
            client.files_upload(
                file=imagefile,
                filename=data["imagefile"],
                initial_comment=message,
                channels=channel_id,
                user_id=user_id,
            )
            os.remove(imagefile)
        elif "embeds_img" in data:
            description = (
                data.get("description", "")
                .replace("[Interactive](", "")
                .replace(".html)", ".html\n\n")
            )
            title = data["title"] if "titles" not in data else data["titles"][0]
            N = 0
            for img in data["images_list"]:
                imagefile = imps.IMG_DIR.joinpath(img).__str__()
                if N == 0:
                    message = f"{title}\n{description}"
                    payload = {
                        "channel": channel_id,
                        "username": user_id,
                        "text": message,
                    }
                    client.chat_postMessage(**payload)
                    title = ""
                if N < len(title) and N != 0:
                    title = data["titles"][N] if "titles" in data else ""
                client.files_upload(
                    file=imagefile,
                    filename=img,
                    initial_comment=title,
                    channels=channel_id,
                    user_id=user_id,
                )
                N += 1
                os.remove(imagefile)
        elif "description" in data:
            title = data.get("title", "")
            description = data.get("description")
            if isinstance(description, List):
                clean_desc = description[0].replace("Page ", "")
            else:
                clean_desc = description.replace("Page ", "")
            message = f"{title}\n{clean_desc}"
            payload = {"channel": channel_id, "username": user_id, "text": message}
            client.chat_postMessage(**payload)

    def telegram(self, func, message, bot, cmd, *args, **kwargs):
        data = func(*args, **kwargs)
        if "imagefile" in data:
            imagefile = imps.IMG_DIR.joinpath(data["imagefile"])
            title = data["title"]
            description = (
                data.get("description", "")
                .replace("[Interactive](", "")
                .replace(".html)", ".html\n\n")
            )
            res = f"{title}\n{description}"
            bot.reply_to(message, res)
            with open(imagefile, "rb") as image:
                bot.reply_to(message, data["title"])
                bot.send_photo(message.chat.id, image)
            os.remove(imagefile)
        elif "embeds_img" in data:
            res_title = data["title"] if "titles" not in data else data["titles"][0]
            N = 0
            for img in data["images_list"]:
                imagefile = imps.IMG_DIR.joinpath(img)
                if N == 0:
                    description = (
                        data.get("description", "")
                        .replace("[Interactive](", "")
                        .replace(".html)", ".html\n\n")
                    )
                    res_title = f"{res_title}\n{description}"
                if N < len(res_title) and N != 0:
                    res_title = data["titles"][N] if "titles" in data else ""
                with open(imagefile, "rb") as image:
                    bot.reply_to(message, res_title)
                    bot.send_photo(message.chat.id, image)
                N += 1
                os.remove(imagefile)
        elif "description" in data:
            title = data.get("title", "")
            description = (
                data.get("description")
                .replace("[Interactive](", "")
                .replace(".html)", ".html\n\n")
            )
            if isinstance(description, List):
                clean_desc = description[0].replace("Page ", "")
            else:
                clean_desc = description.replace("Page ", "")
            res = f"{title}\n{clean_desc}"
            bot.reply_to(message, res)
