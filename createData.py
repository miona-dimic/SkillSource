from application import db
from application import Organisation
from application import Job, IndividualSkill
from application import User
from application import Skill
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

db.create_all()

maria = User( 
            public_id = str(uuid.uuid4()), 
            name = 'Maria Johnson', 
            email = 'maria.john@example.com',
            username = 'maria123', 
            password = generate_password_hash('maria123')
        ) 
db.session.add(maria)
db.session.commit()


#data for jobs
ibm = Organisation(name ='IBM')
google = Organisation(name='Google')
amazon = Organisation(name='Amazon')
microsoft = Organisation(name ='Microsoft')
db.session.add(ibm)
db.session.add(google)
db.session.add(amazon)
db.session.add(microsoft)
db.session.commit()

uni_decription_text = 'Lorem ipsum'

#data for jobs
job1 = Job(title=amazon.name +' - ' + 'Web Developer',description =uni_decription_text,image ='x.png',category='Web Engineering',organisation_id =amazon.id)
job2 =Job (title=ibm.name + ' - ' + 'Software Engineer', description =uni_decription_text, image = 'y.png', category = 'Software Engineering', organisation_id=ibm.id)
job3 =Job (title=ibm.name + ' - ' +'Web Developer', description =uni_decription_text, image = 'z.png', category = 'Web Engineering', organisation_id=ibm.id)
db.session.add(job1)
db.session.add(job2)
db.session.add(job3)
db.session.commit()

skill1 = Skill(name='Backend')
skill2 = Skill(name='UX')
skill3 = Skill(name='Frontend')
skill4 = Skill(name='UI')
skill5 = Skill(name='Visual Design')

db.session.add(skill1)
db.session.add(skill2)
db.session.add(skill3)
db.session.add(skill4)
db.session.add(skill5)
db.session.commit()

job1.skills.append(skill1)
job2.skills.append(skill1)
job2.skills.append(skill2)
job3.skills.append(skill2)

db.session.add(job1)
db.session.add(job2)
db.session.add(job3)
db.session.commit()

userSkill1 = IndividualSkill(skill_id=skill1.id, user_id=maria.id, rating='2/5', change='-1')
userSkill2 = IndividualSkill(skill_id=skill2.id, user_id=maria.id, rating='5/5', change='0')
userSkill3 = IndividualSkill(skill_id=skill3.id, user_id=maria.id, rating='3/5', change='-2')
userSkill4 = IndividualSkill(skill_id=skill4.id, user_id=maria.id, rating='2/5', change='0')
userSkill5 = IndividualSkill(skill_id=skill5.id, user_id=maria.id, rating='3/5', change='0')

maria.skills.append(userSkill1)
maria.skills.append(userSkill2)
maria.skills.append(userSkill3)
maria.skills.append(userSkill4)
maria.skills.append(userSkill5)


db.session.add(userSkill1)
db.session.add(userSkill2)
db.session.add(userSkill3)
db.session.add(userSkill4)
db.session.add(userSkill5)

db.session.add(maria)
db.session.commit()
