import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import BytesIO
import base64

def generate_plots(collection):
    htmls = []
    html1 = top_10_genres(collection)
    htmls.append(html1)
    html2 = movies_by_ratings(collection)
    htmls.append(html2)
    html3 = movies_by_countries(collection)
    htmls.append(html3)
    html4 = budget_vs_gross(collection)
    htmls.append(html4)
    return htmls

def top_10_genres(collection):    
    # Define the pipeline to group by the "genre" field and count the number of documents in each group
    pipeline = [
        {"$group": {"_id": "$genre", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    # Execute the pipeline and extract the group names and count values from the result
    result = collection.aggregate(pipeline)
    groups = []
    counts = []
    for doc in result:
        groups.append(doc['_id'])
        counts.append(doc['count'])

    # Set the figure size
    plt.figure(figsize=(8, 8))

    # Create a pie chart to visualize the count of documents in each group
    plt.pie(counts, labels=groups, autopct='%1.1f%%')
    plt.title("Top 10 Genres")

    # save the plot as a bytes object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # encode the bytes object as a base64 string
    image_string = base64.b64encode(buffer.getvalue()).decode()
    
    # construct the HTML string with the base64-encoded image
    html = f'<img src="data:image/png;base64,{image_string}" alt="My Plot">'
    
    return html
    
def movies_by_ratings(collection):
    # Count of movies by Rating

# Define the pipeline to group by the "genre" field and count the number of documents in each group
    pipeline = [
        {"$group": {"_id": "$rating", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    # Execute the pipeline and extract the group names and count values from the result
    result = list(collection.aggregate(pipeline))

    dfc = pd.DataFrame(result)

    # Set the figure size
    plt.figure(figsize=(10, 6))

    # Create a grouped bar chart to visualize the count of documents in each group
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    sns.barplot(x="_id", y="count", data=dfc)
    plt.title("Movies by Ratings")
    plt.xlabel("Ratings")
    plt.ylabel("Count")
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_string = base64.b64encode(buffer.getvalue()).decode()
    html = f'<img src="data:image/png;base64,{image_string}" alt="My Plot">'
    
    return html

def movies_by_countries(collection):
    # Count of movies by countries

# Define the pipeline to group by the "genre" field and count the number of documents in each group
    pipeline = [
        {"$group": {"_id": "$country", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    # Execute the pipeline and extract the group names and count values from the result
    result = list(collection.aggregate(pipeline))

    dfc = pd.DataFrame(result)

    # Set the figure size
    plt.figure(figsize=(12, 6))

    # Create a grouped bar chart to visualize the count of documents in each group
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    sns.barplot(x="_id", y="count", data=dfc)
    plt.title("Movies by Countries")
    plt.xlabel("Country")
    plt.ylabel("Count")
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_string = base64.b64encode(buffer.getvalue()).decode()
    html = f'<img src="data:image/png;base64,{image_string}" alt="My Plot">'
    
    return html

def budget_vs_gross(collection):
    # Budget vs Gross of movies more than 1M

    # criteria for documents with budget greater than 10 million
    criteria = {"budget": {"$gt": 10000000}}

    result = collection.find(criteria, {"budget": 1, "gross": 1}).sort("gross", -1).limit(50)

    # Convert the result to a pandas DataFrame
    data = []
    for x in result:
        data.append({"Budget": x["budget"], "Gross": x["gross"]})
    dfc = pd.DataFrame(data)

    # Set the figure size
    plt.figure(figsize=(10, 6))
    
    # Create a scatter plot of budget versus gross revenue using seaborn
    sns.scatterplot(data=dfc, x="Budget", y="Gross")
    plt.title("Budget vs. Gross")
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_string = base64.b64encode(buffer.getvalue()).decode()
    html = f'<img src="data:image/png;base64,{image_string}" alt="My Plot">'
    
    return html