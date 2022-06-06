import wrangles
import pandas as pd


#
# Column
#
df_test_create_column = pd.DataFrame([['data1', 'data2']], columns=['column1', 'column2'])

def test_create_column():
    recipe = """
    wrangles:
        - create.column:
            output: column3
    """
    df = wrangles.pipeline.run(recipe, dataframe=df_test_create_column)
    assert len(df.columns) == 3

#
# Index
#
    
df_test_create_index = pd.DataFrame([['one', 'two'], ['une', 'deux'], ['uno', 'dos']], columns=['column1', 'column2'])

def test_create_index():
    recipe = """
        wrangles:
            - create.index:
                output: index_col
                start: 1
                
        """
    df = wrangles.pipeline.run(recipe, dataframe=df_test_create_index)
    assert df.iloc[-1]['index_col'] == 3

#
# GUID
#
df_guid = pd.DataFrame({
    'Product': ['A', 'B'],
})

def test_guid():
    recipe = """
    wrangles:
        - create.guid:
            output: GUID Col
    """
    # Using IESA Commodity
    df = wrangles.pipeline.run(recipe, dataframe=df_guid)
    assert 'GUID Col' in list(df.columns)
    
#
# UUID
#
def test_uuid():
    recipe = """
    wrangles:
        - create.uuid:
            output: UUID Col
    """
    # Using IESA Commodity
    df = wrangles.pipeline.run(recipe, dataframe=df_guid)
    assert 'UUID Col' in list(df.columns)
