import os
from modules.vector_store import load_vector_store

def check_folder(folder_name):
    if os.path.exists(folder_name):
        files = os.listdir(folder_name)
        print(f"📂 {folder_name} contains {len(files)} file(s): {files}")
    else:
        print(f"⚠️ {folder_name} does not exist")

def check_index(index_name):
    if os.path.exists(index_name):
        files = os.listdir(index_name)
        print(f"📦 {index_name} contains: {files}")
        try:
            vs = load_vector_store(index_name)
            if vs:
                results = vs.similarity_search("test", k=1)
                print(f"✅ Index {index_name} is loaded. Sample search returned {len(results)} result(s).")
                # ✅ Show how many chunks are stored
                print(f"📊 Index {index_name} contains {len(vs.index_to_docstore_id)} chunks")
            else:
                print(f"⚠️ Index {index_name} could not be loaded.")
        except Exception as e:
            print(f"❌ Error loading {index_name}: {e}")
    else:
        print(f"⚠️ {index_name} folder does not exist")

if __name__ == "__main__":
    print("=== Checking uploaded folders ===")
    check_folder("data/SOR")
    check_folder("data/SOP")
    check_folder("data/O&M")

    print("\n=== Checking FAISS indexes ===")
    check_index("SOR_index")
    check_index("combined_ops_index")
