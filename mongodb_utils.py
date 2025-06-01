from pymongo import MongoClient
import plotly.express as px
import pandas as pd
import config

def get_focus_figure(keyword):
    with MongoClient(config.MONGODB_URI) as client:
        try:
            database = client.get_database("academicworld")
            faculty = database.get_collection("faculty")
            publications = database.get_collection("publications")
            pub_pipeline = []
            pub_pipeline.append({
                "$project": {
                    "id": 1, 
                    "year": 1, 
                    "keywordScore": {
                        "$ifNull": [
                            {
                                "$first": {
                                    "$map": {
                                        "input": {
                                            "$filter": {
                                                "input": "$keywords", 
                                                "cond": {"$eq": ["$$this.name", keyword]}
                                            }
                                        },
                                        "in": "$$this.score"
                                    }
                                }
                            }, 
                            0
                        ]
                    },
                    "totalScore": {"$sum": "$keywords.score"}, 
                }
            })
            fac_pipeline = []
            fac_pipeline.extend([
                {"$match": {"keywords.name": keyword}},
                {"$project": {"publications": 1}}
            ])
            fac_pipeline.append({
                "$lookup": {
                    "from": "publications",
                    "localField": "publications",
                    "foreignField": "id",
                    "pipeline": pub_pipeline,
                    "as": "publications"
                }
            })
            fac_pipeline.extend([
                {"$unwind": {"path": "$publications"}},
                {"$group": {
                    "_id": "$publications.year",
                    "keywordScoreYearly": {"$sum": "$publications.keywordScore"},
                    "totalScoreYearly": {"$sum": "$publications.totalScore"}
                }},
                {"$project": {
                    "year": "$_id",
                    "focus": {
                        "$cond": {
                            "if": {"$gt": ["$totalScoreYearly", 0]},
                            "then": {"$divide": ["$keywordScoreYearly", "$totalScoreYearly"]},
                            "else": 0
                        }
                    },
                    "_id": 0
                }},
                {"$match": {"year": {"$gt": 0}}},
                {"$sort": {"year": 1}}
            ])
            result = faculty.aggregate(fac_pipeline)
            year, focus = [], []
            curYear = 0
            for r in result:
                if curYear:
                    if r['year'] == curYear:
                        year.append(r['year'])
                        focus.append(r['focus'])
                    else:
                        year.append(curYear)
                        focus.append(0)
                    curYear += 1
                else:
                    if r['focus'] > 0:
                        year.append(r['year'])
                        focus.append(r['focus'])
                        curYear = r['year'] + 1
            df = pd.DataFrame(data={'year': year, 'focus': focus})
            fig = px.line(df, x='year', y='focus', markers=True)
            return fig
        except Exception as e:
            raise Exception("Unable to find the document due to the following error: ", e)
