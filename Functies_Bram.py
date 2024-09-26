def omloopplanning_buslijn(omloopplanning):
    omloopplanning['buslijn'] = omloopplanning['buslijn'].fillna('##')
    for i in range(len(omloopplanning)):
        if omloopplanning['activiteit'][i]=='materiaal rit':
            omloopplanning['buslijn'][i].replace('##','materiaalrit')
    omloopplanning['buslijn'] = omloopplanning['buslijn'].apply(lambda x: int(x) if isinstance(x, float) else x)

def afstandcode_maken(omloopplanning):
    omloopplanning['afstandcode']=''
    for i in range(len(omloopplanning)):
        omloopplanning['afstandcode'][i]=f"{omloopplanning['startlocatie'][i]}{omloopplanning['eindlocatie'][i]}{omloopplanning['buslijn'][i]}"