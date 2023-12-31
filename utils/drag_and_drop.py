import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, JsCode

def build_dad(df, zones):
    # JavaScript functions for row manipulation
    onRowDragEnd = JsCode("""
    function onRowDragEnd(e) {
        console.log('onRowDragEnd', e);
    }
    """)

    getRowNodeId = JsCode("""
    function getRowNodeId(data) {
        return data.id;
    }
    """)

    onRowDragMove = JsCode("""
    function onRowDragMove(event) {
        var movingNode = event.node;
        var overNode = event.overNode;

        var rowNeedsToMove = movingNode !== overNode;

        if (rowNeedsToMove) {
            var movingData = movingNode.data;
            var overData = overNode.data;

            immutableStore = newStore;

            var fromIndex = immutableStore.indexOf(movingData);
            var toIndex = immutableStore.indexOf(overData);

            var newStore = immutableStore.slice();
            moveInArray(newStore, fromIndex, toIndex);

            immutableStore = newStore;
            gridOptions.api.setRowData(newStore);

            gridOptions.api.clearFocusedCell();
        }

        function moveInArray(arr, fromIndex, toIndex) {
            var element = arr[fromIndex];
            arr.splice(fromIndex, 1);
            arr.splice(toIndex, 0, element);
        }
    }
    """)

    # Building grid options
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(rowDrag=True, rowDragManaged=True, rowDragEntireRow=True)
    gb.configure_column('zone', editable=True, 
                        cellEditor='agSelectCellEditor',
                        cellEditorParams={'values': zones})  # Configuring the first column as editable with a select box
    gb.configure_grid_options(
        rowDragManaged=True,
        onRowDragEnd=onRowDragEnd,
        deltaRowDataMode=True,
        getRowNodeId=getRowNodeId,
        animateRows=True,
        onRowDragMove=onRowDragMove
    )
    gridOptions = gb.build()

    # Display the draggable grid in Streamlit
    data = AgGrid(
        df,
        gridOptions=gridOptions,
        allow_unsafe_jscode=True,
        update_mode=GridUpdateMode.MANUAL
    )

    return data['data']  # st.write(data['data'])

# old:
# import streamlit as st  # pip install streamlit=1.12.0
# import pandas as pd
# from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, JsCode # pip install streamlit-aggrid==0.2.3

# def build_dad(df):
#     onRowDragEnd = JsCode("""
#     function onRowDragEnd(e) {
#         console.log('onRowDragEnd', e);
#     }
#     """)

#     getRowNodeId = JsCode("""
#     function getRowNodeId(data) {
#         return data.id
#     }
#     """)

#     onGridReady = JsCode("""
#     function onGridReady() {
#         immutableStore.forEach(
#             function(data, index) {
#                 data.id = index;
#                 });
#         gridOptions.api.setRowData(immutableStore);
#         }
#     """)

#     onRowDragMove = JsCode("""
#     function onRowDragMove(event) {
#         var movingNode = event.node;
#         var overNode = event.overNode;

#         var rowNeedsToMove = movingNode !== overNode;

#         if (rowNeedsToMove) {
#             var movingData = movingNode.data;
#             var overData = overNode.data;

#             immutableStore = newStore;

#             var fromIndex = immutableStore.indexOf(movingData);
#             var toIndex = immutableStore.indexOf(overData);

#             var newStore = immutableStore.slice();
#             moveInArray(newStore, fromIndex, toIndex);

#             immutableStore = newStore;
#             gridOptions.api.setRowData(newStore);

#             gridOptions.api.clearFocusedCell();
#         }

#         function moveInArray(arr, fromIndex, toIndex) {
#             var element = arr[fromIndex];
#             arr.splice(fromIndex, 1);
#             arr.splice(toIndex, 0, element);
#         }
#     }
#     """)
#     gb = GridOptionsBuilder.from_dataframe(df)
#     gb.configure_default_column(rowDrag = False, rowDragManaged = True, rowDragEntireRow = False, rowDragMultiRow=True)
#     gb.configure_column('bloco', rowDrag = True, rowDragEntireRow = True)
#     gb.configure_grid_options(rowDragManaged = True, 
#                               onRowDragEnd = onRowDragEnd, 
#                               deltaRowDataMode = True, 
#                               getRowNodeId = getRowNodeId, 
#                               onGridReady = onGridReady, 
#                               animateRows = True, 
#                               onRowDragMove = onRowDragMove)
#     gridOptions = gb.build()

#     data = AgGrid(df,
#                 gridOptions=gridOptions,
#                 allow_unsafe_jscode=True,
#                 update_mode=GridUpdateMode.MANUAL
#     )

#     return data['data']