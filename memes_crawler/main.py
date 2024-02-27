from crawler import Memes
from mongo import MongoDB

if __name__ == "__main__":
    memes = Memes()
    download_result = memes.main()

    mongo_clinet = MongoDB()
    print(mongo_clinet.create_data(download_result))
    # print(mongo_clinet.delete_data())
    # print(mongo_clinet.update_date({"name": "AAAAAAAAAA"}, {"name": {"$regex": "DrakeNoYes"}}))