
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.io as pio
pio.renderers.default = 'notebook'   # or 'colab' for Google Colab


def forecaster(df):

    print(df.head(10))
    print(df.tail(10))
    print("Any NaNs?", df.isna().any())
    print("Any zeros?", (df['y'] == 0).sum())
    
    model = Prophet(
        daily_seasonality = "auto",
        weekly_seasonality = True,
        yearly_seasonality = True
    )
    model.fit(df)

    future = model.make_future_dataframe(periods= FORECAST_DAYS, freq="W")
    forecast_full = model.predict(future)
    forecast = forecast_full[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    # Figures
    fig1 = model.plot(forecast_full)
    fig2 = model.plot_components(forecast_full)
    fig3 = plot_plotly(model, forecast_full)


    return future, forecast, fig1 , fig2, fig3

# usage 
# future_df , forecast_df, fig1, fig2, fig3 = forecaster(composite_df)


def regime_chart(df):
    cutoff_date = df["ds"].max() - pd.Timedelta(days= FORECAST_DAYS)

    regime_colors = {
        "Spike":             "#c8f7c5",
        "Building":          "#fef9c3",
        "Quiet":             "#f0f0f0",
        "Collapsing":        "#fdd",
        "Insufficient Data": "#ffffff"
    }

    fig, (ax1, ax2) = plt.subplots(
            2, 1,
            figsize= (14, 7),
            sharex= True,
            gridspec_kw= {"height_ratios": [2,1]}
    )

    # Background regime shade 
    for i in range (len(df["regime"]) - 1):

        regime = df["regime"].iloc[i]
        ax1.axvspan(
            df["ds"].iloc[i],
            df["ds"].iloc[i + 1],
            color= regime_colors.get(regime, "#ffffff")
        )
    
    # Main trend line
    ax1.plot(
        df["ds"],
        df["y"],
        color= "#1a1a2e",
        linewidth= 4,
        label = "Trend Score"
    )
    ax1.set_ylabel("Trend Score")
    ax1.set_title(
        f"Regime Classification - Last 90 Days for {KEYWORD}",
        fontsize= 14,
        fontweight= "bold"
    )
    ax1.grid(alpha= 0.3)

    
    # Z-Score Velocity 
    ax2.plot(
        df["ds"],
        df["short_velocity_zscore"],
        color= "tomato",
        linewidth= 2,
        label= f"Short Z-score"
    )

    ax2.plot(
        df["ds"],
        df["long_velocity_zscore"],
        color= "steelblue",
        linewidth= 2,
        label= "Long Z-score"
    )

    ax2.axhline(
        y=SPIKE_THRESHOLD,
        color= "green",
        linestyle= "--",
        alpha = 0.7,
        linewidth= 1,
        label= f"Spike Threshold (Z={SPIKE_THRESHOLD})"
    )

    ax2.axhline(
        y= COLLAPSE_THRESHOLD,
        color= "red",
        linestyle= "--",
        alpha= 0.7,
        linewidth= 1,
        label= f"Building Threshold (Z={BUILD_THRESHOLD})"
    )

    ax2.axhline(
        y= 0,
        color= "gray",
        linestyle= "-",
        alpha= 0.7,
        linewidth= 1
    )

    ax2.set_ylabel("Z-Score")
    ax2.set_xlabel("Date")
    ax2.legend(fontsize= 10)
    ax2.grid(alpha= 0.3)

    # Regime legend
    patches = [
        mpatches.Patch(color="#c8f7c5", label="Spike: Act Now"),
        mpatches.Patch(color="#fef9c3", label="Building: Watch"),
        mpatches.Patch(color="#f0f0f0", label="Quiet: Wait"),
        mpatches.Patch(color="#fdd",    label="Collapsing: Hold")
    ]
    
    ax1.legend(handles=patches, loc="upper left", fontsize=10)
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    plt.xticks(rotation= 45)
    plt.tight_layout()

    return fig



# regime_chart(velocity_df)