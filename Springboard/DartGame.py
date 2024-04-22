import pandas as pd
from io import StringIO

def game_dart(input_results):
  csvresutls = StringIO(input_results)
  df = pd.read_csv(csvresutls, sep=',', lineterminator='\n', header=None)
  df.columns=['Player','Points']
  total_points = df.groupby('Player')['Points'].sum().sort_index()
  throws = df.groupby('Player')['Player'].count().sort_index()
  max_points = df.groupby('Player')['Points'].max().sort_index()
  min_points = df.groupby('Player')['Points'].min().sort_index()
  mean_points = df.groupby('Player')['Points'].mean().sort_index()
  pl = df['Player'].sort_values().unique()
  res ={'Player': pl, 'Total Points':list(total_points),'Throws': list(throws), 'Max points': list(max_points), 'Min points': list(min_points), 'Mean points': list(mean_points) }
  res_df = pd.DataFrame(res)
  return res_df


print(game_dart('a,1 \nb,2 \na,2 \nd,5 \nb,2 \na,4 \nb,4 \nc,1 \nb, 3'))
