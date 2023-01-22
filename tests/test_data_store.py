from flowrunner.data_store import DataStore

def test_data_store():
    data_store = DataStore()
    data_store.store_data("test", 123)
    assert data_store.read_data("test") == 123