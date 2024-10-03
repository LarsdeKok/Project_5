def omloopplanning_buslijn(omloopplanning):
    '''
    Replaces the empty cells in 'buslijn' with the corresponding 'activiteit'
    '''
    omloopplanning['buslijn'] = omloopplanning['buslijn'].fillna('##')
    for i in range(len(omloopplanning)):
        if omloopplanning['activiteit'][i]=='materiaal rit':
            omloopplanning['buslijn'][i]=omloopplanning['buslijn'][i].replace('##','materiaalrit')
        if omloopplanning['activiteit'][i]=='opladen':
            omloopplanning['buslijn'][i]=omloopplanning['buslijn'][i].replace('##','opladen')
        if omloopplanning['activiteit'][i]=='idle':
            omloopplanning['buslijn'][i]=omloopplanning['buslijn'][i].replace('##','idle')
    omloopplanning['buslijn'] = omloopplanning['buslijn'].apply(lambda x: int(x) if isinstance(x, float) else x)

def afstandcode_maken(omloopplanning):
    '''
    Creates a new column called 'afstandcode' which corresponds to the afstandcode in the dictionary
    '''
    omloopplanning['afstandcode']=''
    for i in range(len(omloopplanning)):
        omloopplanning['afstandcode'][i]=f"{omloopplanning['startlocatie'][i]}{omloopplanning['eindlocatie'][i]}{omloopplanning['buslijn'][i]}"

def energieverbruik_berekenen(omloopplanning, afstand:dict, rijdend_verbruik:float):
    '''
    Creates a new column called 'energieverbruik2' which contains the newly calculated energy usage
    '''
    omloopplanning['energieverbruik2']=''
    for i in range(len(omloopplanning)):
        if 'idle' in omloopplanning['afstandcode'][i]:
            omloopplanning['energieverbruik2'][i]=0.01
        elif 'opladen' in omloopplanning['afstandcode'][i]:
            omloopplanning['energieverbruik2'][i]=-1
        else:
            omloopplanning['energieverbruik2'][i]=(afstand[omloopplanning['afstandcode'][i]]/1000)*rijdend_verbruik