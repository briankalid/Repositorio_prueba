from datetime import datetime
from datetime import date


def update_data(followerstr,rtsstr,favstr):
    try:
        current_date = date.today()

        filedate= open('data/time.txt','r+')
        last_date_file=list(filedate)[-1][:-1]
        last_date_file = datetime.strptime(last_date_file,"%d/%m/%Y")


        file1= open('data/maxfollow.txt','r')

        file2= open('data/maxrts.txt','r')

        file3= open('data/maxfvs.txt','r')

        if last_date_file.date()==current_date:
            fp1 = list(file1)
            today_follow_file=int(fp1[-1][:-1])
            file1.close()

            if int(followerstr) > today_follow_file:
                fp1.pop()
                fp1.append(followerstr)
                file1= open('data/maxfollow.txt','w+')
                for follow in fp1:
                    print(follow)
                    file1.write(str(follow[::1]).rstrip('\n')+'\n')


            fp2 = list(file2)
            today_rts_file=int(fp2[-1][:-1])
            file2.close()

            if int(rtsstr) > today_rts_file:
                fp2.pop()
                fp2.append(rtsstr)
                file2= open('data/maxrts.txt','w+')
                for rts in fp2:
                    print(rts)
                    file2.write(str(rts[::1]).rstrip('\n')+'\n')



            fp3 = list(file3)
            today_fvs_file=int(fp3[-1][:-1])
            file3.close()

            if int(favstr) > today_fvs_file:
                fp3.pop()
                fp3.append(favstr)
                file3= open('data/maxfvs.txt','w+')
                for fvs in fp3:
                    print(str(fvs))
                    file3.write(str(fvs[::1]).rstrip('\n')+'\n')


        else:
            filedate.write(current_date.strftime("%d/%m/%Y")+"\n")
            file1= open('data/maxfollow.txt','a')
            file2= open('data/maxrts.txt','a')
            file3= open('data/maxfvs.txt','a')
            file1.write(followerstr + "\n")
            file2.write(rtsstr + "\n")
            file3.write(favstr + "\n")

        filedate.close()
        file1.close()
        file2.close()
        file3.close()

    except:
        file1= open('data/maxfollow.txt','a')
        file1.write(followerstr + "\n")
        file1.close()

        file2= open('data/maxrts.txt','a')
        file2.write(rtsstr + "\n")
        file2.close()

        file3= open('data/maxfvs.txt','a')
        file3.write(favstr + "\n")
        file3.close()

        d1 = date.today().strftime("%d/%m/%Y")

        filedate= open('data/time.txt','a')
        filedate.write(d1 + "\n")
        filedate.close()
