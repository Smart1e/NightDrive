def toDatabaseHDD(partTypeID):
    import fmrest
    fms = fmrest.Server('https://db.teamrm5.co.uk',
                        user='FileMakerAPIAccount',
                        password='@pp1eRMFR',
                        database='The Database',
                        layout='Parts',
                        api_version='vLatest')
    
    fms.login()
    newRecord = {
        'PartTypeID' : partTypeID,
        'Supplier' : "Mac Breakdown",
        'OrderNo' : "N/A",
        'cost' : "0"
    }
    fms.create_record(field_data=newRecord)
    fms.logout()
    return 'success'

def getMostRecentPart():
    import fmrest
    fms = fmrest.Server('https://db.teamrm5.co.uk',
                        user='FileMakerAPIAccount',
                        password='@pp1eRMFR',
                        database='The Database',
                        layout='Parts',
                        api_version='vLatest')
    
    fms.login()
    # Get the most recent record
    order_by = [{'fieldName': 'PartID', 'sortOrder': 'descend'}]
    query = [{'PartID': 'P*'}]
    foundset = fms.find(query=query, sort=order_by, limit=1)
    fms.logout()
    return foundset[0].values()[0]
    
def returnPartTypeID(diskInfoDict):
    databaseTypeIDs = {
    '3.5" HDD 160GB': 'PartType364',
    '3.5" HDD 250GB': 'PartType365',
    '3.5" HDD 320GB': 'PartType366',
    '3.5" HDD 500GB': 'PartType367',
    '3.5" HDD 750GB': 'PartType368',
    
    '3.5" HDD 1TB': 'PartType369',
    '3.5" HDD 2TB': 'PartType370',
    '3.5" HDD 3TB': 'PartType371',
    '3.5" HDD 4TB': 'PartType372',
    
    '2.5" HDD 160GB': 'PartType373',
    '2.5" HDD 250GB': 'PartType374',
    '2.5" HDD 320GB': 'PartType375',
    '2.5" HDD 500GB': 'PartType376',
    '2.5" HDD 750GB': 'PartType377',
    
    '2.5" HDD 1TB': 'PartType378',
    '2.5" HDD 2TB': 'PartType379',
    
    '2.5" SSD 128GB': 'PartType380',
    '2.5" SSD 256GB': 'PartType381',
    '2.5" SSD 512GB': 'PartType382',
    
    '2.5" SSD 1TB': 'PartType383',
    '2.5" SSD 2TB': 'PartType384',
    '2.5" SSD 4TB': 'PartType385',
}
    for key, value in zip(databaseTypeIDs.keys(), databaseTypeIDs.values()):
        if key == diskInfoDict['diskGirth'] + " " + diskInfoDict['diskType'] + " " + diskInfoDict['diskSize']:
            return value
    else:
        return "Not in the Database"
if __name__ == '__main__':
    print(getMostRecentPart() + "is the most recent part.")
    
    