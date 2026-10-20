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