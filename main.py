from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt 


# Fetch query form pytrends  
def fetch_raw(KEYWORD):
    search_df = fetch_trends(KEYWORD, gprop="")
    youtube_df = fetch_trends(KEYWORD, gprop="youtube")
    news_df = fetch_trends(KEYWORD, gprop="news")

    # Fetch recommended queries 

    # Clean dataframe 
    cleaned_search = prepare_df(search_df, "search", KEYWORD)
    cleaned_youtube = prepare_df(youtube_df, "youtube", KEYWORD)
    cleaned_news = prepare_df(news_df, "news", KEYWORD)


    # Combine dataframe
    return combined_df = pd.concat(
        [cleaned_search, cleaned_youtube, cleaned_news],
        ignore_index=True
    )

# combined_df = combined_df.sort_values("date").reset_index(drop=True)
# print(combined_df)

# Save dataframe 
combined_df.to_csv(f"/home/szasz/Documents/CS/code/signal_flow/combined_trends_{KEYWORD}.csv", index=False)

# Join the dtaframes with "ds" and "y" columns
composite_df = composite(combined_df)
print(composite_df.head())

# Get velocity and Z-score
velocity_df = velocity(composite_df, WINDOWS)
print(velocity_df.head(10))


# Get regime 
velocity_df["regime"] = velocity_df.apply(classify_regime, axis = 1) 
print(f" regime value counts {velocity_df["regime"].value_counts()}")
print(velocity_df.head())

# Forecasting 
future_df , forecast_df, fig1, fig2, fig3 = forecaster(composite_df)

# Plotting 
# Plotting three singals 
three_singal_plot = plot_singals()
three_singal_plot = fig4
fig4

# Regime plot
regime_plot = regime_chart(velocity_df)

# Save plots to pdf 
with PdfPages(f"{KEYWORD}_report.pdf") as pdf:

    regime_plot_save = regime_chart(velocity_df)
    signals_plot_save = plot_singals()

    pdf.savefig(regime_plot_save)
    pdf.savefig(signals_plot_save)
    pdf.savefig(fig1)
    pdf.savefig(fig2)

    plt.close(regime_plot_save)
    plt.close(singals_plot_save)
    plt.close(fig1)
    plt.close(fig2)
    print("All charts saved sucessfully!")