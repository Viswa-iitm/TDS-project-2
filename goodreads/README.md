# Data Analysis Report: Goodreads

## Dataset Overview
With an expansive dataset of 10,000 rows focused on books, this analysis delves deep into understanding readers' interactions and sentiments surrounding their favorite titles. Each entry encapsulates a unique book, complete with its identity markers (like ISBN, titles, authors), user engagement metrics (ratings and reviews), and bibliographic details (like publication year and language).

### Key Insights

1. **Rating Overview**: The average rating across the dataset stands at a commendable 4.00, indicating that readers generally respond positively to the books they choose. This positive feedback extends across the ratings spectrum, with users distributing their ratings as follows:
   - **1-Star**: Approximately 1,345
   - **2-Star**: About 3,111
   - **3-Star**: Roughly 11,476
   - **4-Star**: Around 19,966
   - **5-Star**: Around 23,790
   The high number of 4 to 5-star ratings suggests a healthy level of satisfaction amongst readers.

2. **Engagement Levels**: Books generally attract a significant number of ratings, with an average count of over 54,000. This high level of engagement could indicate an active reading community or popular genres within the dataset.

3. **Publication Year Trends**: Most books in the dataset were originally published around the early 2000s, with the data showing a collected mean publication year around 1982. Despite this, there are entries as recent as 2017. The presence of older titles alongside newer works suggests fluctuations in reader interest and reprints of classic literature could be at play.

4. **Correlations and Implications**: A deeper dive into the correlation matrix reveals notable relationships:
   - **Ratings and Reviews**: There�s a strong correlation (0.99) between *ratings_count* and *work_ratings_count*, implying that books that receive many ratings also garner high overall ratings, likely resulting in a more engaged reader base who participate in leaving reviews.
   - **Books Count and Ratings**: Interestingly, the *books_count* negatively correlates with ratings (around -0.26). This insight could suggest that books with more editions or versions might be inherently rated lower, perhaps due to variations in perception according to differences in publication or editions.

5. **Missing Data**: There appears to be significant gaps in ISBN and original titles, with 700 missing ISBNs and 585 missing original titles. This could complicate analyses around book identity verification or bibliographic cross-referencing.

### Potential Implications

- **For Publishers and Authors**: The data indicates that reader engagement is vital for book success, suggesting that marketing efforts should focus on leveraging the networks of existing readers to generate more ratings and reviews.
- **For Readers**: Analyzing the trends of high-rated books from varied publication years can aid reading choices. This dataset could prove to foster book clubs or reading lists that introduce readers to lesser-known but highly rated books.
- **For Educators**: Understanding which older titles still resonate with readers could assist educators in crafting reading lists that blend traditional literature with contemporary interests, tailoring courses that appeal to diverse age groups.
- **For Data Analysts**: The positive response to original literary works could lead to further studies regarding the rediscovery of classics and how they stand the test of time. 

In conclusion, this dataset provides a rich tapestry of book-related data. It not only sheds light on reader preferences and behaviors but also opens new avenues for literary and market exploration. By utilizing these insights, stakeholders across the literary spectrum can align their efforts in ways that resonate with audiences and capitalize on ongoing trends.

## Technical Analysis

### Basic Information
- Total Rows: 10000
- Columns: book_id, goodreads_book_id, best_book_id, work_id, books_count, isbn, isbn13, authors, original_publication_year, original_title, title, language_code, average_rating, ratings_count, work_ratings_count, work_text_reviews_count, ratings_1, ratings_2, ratings_3, ratings_4, ratings_5, image_url, small_image_url
- Column Types: {'book_id': 'int64', 'goodreads_book_id': 'int64', 'best_book_id': 'int64', 'work_id': 'int64', 'books_count': 'int64', 'isbn': 'object', 'isbn13': 'float64', 'authors': 'object', 'original_publication_year': 'float64', 'original_title': 'object', 'title': 'object', 'language_code': 'object', 'average_rating': 'float64', 'ratings_count': 'int64', 'work_ratings_count': 'int64', 'work_text_reviews_count': 'int64', 'ratings_1': 'int64', 'ratings_2': 'int64', 'ratings_3': 'int64', 'ratings_4': 'int64', 'ratings_5': 'int64', 'image_url': 'object', 'small_image_url': 'object'}

### Missing Data
- isbn: 700 missing values
- isbn13: 585 missing values
- original_publication_year: 21 missing values
- original_title: 585 missing values
- language_code: 1084 missing values

### Summary Statistics
#### book_id
{
  "count": 10000.0,
  "mean": 5000.5,
  "std": 2886.8956799071675,
  "min": 1.0,
  "25%": 2500.75,
  "50%": 5000.5,
  "75%": 7500.25,
  "max": 10000.0
}
#### goodreads_book_id
{
  "count": 10000.0,
  "mean": 5264696.5132,
  "std": 7575461.863589611,
  "min": 1.0,
  "25%": 46275.75,
  "50%": 394965.5,
  "75%": 9382225.25,
  "max": 33288638.0
}
#### best_book_id
{
  "count": 10000.0,
  "mean": 5471213.5801,
  "std": 7827329.890719961,
  "min": 1.0,
  "25%": 47911.75,
  "50%": 425123.5,
  "75%": 9636112.5,
  "max": 35534230.0
}
#### work_id
{
  "count": 10000.0,
  "mean": 8646183.4246,
  "std": 11751060.824080039,
  "min": 87.0,
  "25%": 1008841.0,
  "50%": 2719524.5,
  "75%": 14517748.25,
  "max": 56399597.0
}
#### books_count
{
  "count": 10000.0,
  "mean": 75.7127,
  "std": 170.47072765025834,
  "min": 1.0,
  "25%": 23.0,
  "50%": 40.0,
  "75%": 67.0,
  "max": 3455.0
}
#### isbn13
{
  "count": 9415.0,
  "mean": 9755044298883.463,
  "std": 442861920665.57336,
  "min": 195170342.0,
  "25%": 9780316192995.0,
  "50%": 9780451528640.0,
  "75%": 9780830777175.0,
  "max": 9790007672390.0
}
#### original_publication_year
{
  "count": 9979.0,
  "mean": 1981.987674115643,
  "std": 152.57666516754668,
  "min": -1750.0,
  "25%": 1990.0,
  "50%": 2004.0,
  "75%": 2011.0,
  "max": 2017.0
}
#### average_rating
{
  "count": 10000.0,
  "mean": 4.002191000000001,
  "std": 0.25442748053872905,
  "min": 2.47,
  "25%": 3.85,
  "50%": 4.02,
  "75%": 4.18,
  "max": 4.82
}
#### ratings_count
{
  "count": 10000.0,
  "mean": 54001.2351,
  "std": 157369.95643554674,
  "min": 2716.0,
  "25%": 13568.75,
  "50%": 21155.5,
  "75%": 41053.5,
  "max": 4780653.0
}
#### work_ratings_count
{
  "count": 10000.0,
  "mean": 59687.3216,
  "std": 167803.7852374182,
  "min": 5510.0,
  "25%": 15438.75,
  "50%": 23832.5,
  "75%": 45915.0,
  "max": 4942365.0
}
#### work_text_reviews_count
{
  "count": 10000.0,
  "mean": 2919.9553,
  "std": 6124.378131569911,
  "min": 3.0,
  "25%": 694.0,
  "50%": 1402.0,
  "75%": 2744.25,
  "max": 155254.0
}
#### ratings_1
{
  "count": 10000.0,
  "mean": 1345.0406,
  "std": 6635.626262783459,
  "min": 11.0,
  "25%": 196.0,
  "50%": 391.0,
  "75%": 885.0,
  "max": 456191.0
}
#### ratings_2
{
  "count": 10000.0,
  "mean": 3110.885,
  "std": 9717.123578396993,
  "min": 30.0,
  "25%": 656.0,
  "50%": 1163.0,
  "75%": 2353.25,
  "max": 436802.0
}
#### ratings_3
{
  "count": 10000.0,
  "mean": 11475.8938,
  "std": 28546.449183182456,
  "min": 323.0,
  "25%": 3112.0,
  "50%": 4894.0,
  "75%": 9287.0,
  "max": 793319.0
}
#### ratings_4
{
  "count": 10000.0,
  "mean": 19965.6966,
  "std": 51447.35838380058,
  "min": 750.0,
  "25%": 5405.75,
  "50%": 8269.5,
  "75%": 16023.5,
  "max": 1481305.0
}
#### ratings_5
{
  "count": 10000.0,
  "mean": 23789.8056,
  "std": 79768.88561077163,
  "min": 754.0,
  "25%": 5334.0,
  "50%": 8836.0,
  "75%": 17304.5,
  "max": 3011543.0
}

## Visualizations
- [Correlation Heatmap](correlation_heatmap.png)
- [Top Categories - isbn](isbn_top_categories.png)
- [Top Categories - authors](authors_top_categories.png)
- [Top Categories - original_title](original_title_top_categories.png)
- [Top Categories - title](title_top_categories.png)
- [Top Categories - language_code](language_code_top_categories.png)
- [Top Categories - image_url](image_url_top_categories.png)
- [Top Categories - small_image_url](small_image_url_top_categories.png)

## Recommendations
No specific recommendations could be generated.
