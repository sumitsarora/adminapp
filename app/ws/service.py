#from app.ws.level import Level
class Service:

    def constructJsonResponse(self,levelObjArr):
    #print(len(levelObjArr))


        levelList=[]

        level1Local=None
        level2Local=None
        level3Local=None
        level4Local=None
        level5Local=None
        titleLocal=None
        flag=0
        for item in range(len(levelObjArr)):
            level1Local=levelObjArr[item].get_level1()

            if level1Local in ([l1['level1'] for l1 in levelList]):
                continue
            #level.update({'level1':level1Local})
            else:
                levelList.append({'level1':level1Local})
        #levelList.append(level)

        for l1 in range(len(levelList)):
            #print('test ',levelList[l1]['level1'])
            level2=[]
            level3=[]
            level={}

            for l2 in range(len(levelObjArr)):
                #print('level2 ',level2)
                level1Local=levelObjArr[l2].get_level1()
                level2Local=levelObjArr[l2].get_level2()
                if (levelList[l1]['level1']==level1Local):
                    if (level2Local in [a['level'] for a in level2]):
                        continue
                    else:
                        if level2Local!='':
                            level={'level':level2Local}
                            level2.append(level)
            for l2 in level2:

                for l3 in range(len(levelObjArr)):
                    #print('level2 ',level2)
                    level1Local=levelObjArr[l3].get_level1()
                    level2Local=levelObjArr[l3].get_level2()
                    level3Local=levelObjArr[l3].get_level3()
                    #print(level1Local,'$$$$$$$$4',levelList[l1]['level1'])
                    if (level3Local!='' and l2['level']==level2Local and level1Local==levelList[l1]['level1']):

                        if (level3Local in [a['level'] for a in level3]):
                            continue
                        else:
                            level={'level':level3Local}
                            print(levelList[l1]['level1'],' ',l2['level'],' ',level3Local)
                            level3.append(level)

            levelList[l1]['level2']=level2

            for l2 in levelList[l1]['level2']:

                level3=[]
                level={}
                for obj in range(len(levelObjArr)):
                    level1Local=levelObjArr[obj].get_level1()
                    level2Local=levelObjArr[obj].get_level2()
                    level3Local=levelObjArr[obj].get_level3()
                    #level3=[]

                    if level3Local!='' and l2['level']==level2Local  and level1Local==levelList[l1]['level1']:
                        if (level3Local in [a['level'] for a in level3]):
                            continue
                        else:
                            level={'level':level3Local}
                            level3.append(level)
                            #print('level3 ',level3)
                    l2['level3']=level3
                    #print('******level3*******',level2)
            #l2['level3']=level3
                for l3 in l2['level3']:
                    level4=[]
                    level={}
                    for obj in range(len(levelObjArr)):
                        level2Local=levelObjArr[obj].get_level2()
                        level3Local=levelObjArr[obj].get_level3()
                        level4Local=levelObjArr[obj].get_level4()

                        if level4Local!='' and level3Local==l3['level']:
                            if (level4Local in [a['level'] for a in level4]):
                                continue
                            else:
                                level={'level':level4Local}
                                level4.append(level)
                                #print('level3 ',level3)
                        l3['level4']=level4

        return levelList
