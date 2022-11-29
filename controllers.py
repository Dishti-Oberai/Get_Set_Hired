from django.contrib import messages

def shellController():
    from home.models import skill, Skill
    count = len(skill.objects.all())
    skill = skill(title = 'skill' + str(count+1))
    skill.save()

    count = len(Skill.objects.all())
    skill = Skill(title = 'skill' + str(count+1))
    skill.save()

def loginController(req):
    from django.contrib.auth import authenticate, login
    username = req.POST['username']
    password = req.POST['password']
    user = authenticate(req, username=username, password=password)
    if user is not None:
        login(req, user)
        messages.success(req, f"{username} successfully loggedin!")
        context = {'status': True}
        return context

    messages.error(req, 'Please provide correct details.')
    context = {'status': False}
    return context


def userRegisterController(req):
    from home.forms import UserRegisterForm
    from django.contrib.auth.models import User
    from utils import sendFormErrorMessages

    form = UserRegisterForm(req.POST)
    if form.is_valid():
        form.save()

        username = form.cleaned_data.get('username')
        user = User.objects.get(username=username)
        user.userprofile.isUser = True
        user.userprofile.save()

        messages.success(req, f"Account created for {username}!")
        context = {"status": True}
        return context

    sendFormErrorMessages(req, form)
    context = {"status": False}
    return context


def companyRegisterController(req):
    from home.forms import CompanyRegisterForm
    from django.contrib.auth.models import User
    from utils import sendFormErrorMessages

    form = CompanyRegisterForm(req.POST)
    if form.is_valid():
        form.save()

        username = form.cleaned_data.get('username')
        user = User.objects.get(username=username)
        user.companyprofile.isCompany = True
        user.companyprofile.save()

        messages.success(req, f"Account created for {username}!")
        context = {"status": True, "form": form}
        return context

    sendFormErrorMessages(req, form)
    context = {"status": False, "form": form}
    return context


def indexController(req):
    context = {"status": True}
    from home.models import Notification 
    if req.user.userprofile.isUser:
        context["image"] = req.user.userprofile.image
        context["page"] = 'home/index_student.html'
    else:
        from home.models import JobPosting
        jobPostings_closed = JobPosting.objects.all().filter(status = 'closed').filter(company = req.user.id)
        jobPostings_open = JobPosting.objects.all().filter(status = 'open').filter(company = req.user.id)
        context["jobPostings_open"] = jobPostings_open
        context["jobPostings_closed"] = jobPostings_closed
        context["page"] = 'home/index_startup.html'
    context["notifications"] = Notification.objects.filter(reciever = req.user).order_by('-time')
    return context


def profileController(req, profileId):
    from home.models import UserProfile, CompanyProfile, Feedback
    profile = UserProfile.objects.get(id=profileId)
    user = profile.isUser

    if user:
        page = 'home/profile_student.html'
    else:
        user = False
        page = 'home/profile_startup.html'
        profile = CompanyProfile.objects.get(id=profileId)
    context = {"status": True, "user": profile.user, "profile": profile, "page": page}

    if user:
        linkedInFeedback = Feedback.objects.all().filter(user__in = [profile.user.id]).filter(company__in = [req.user], ratingfield = "LinkedIn").first()
        resumeFeedback = Feedback.objects.all().filter(user__in = [profile.user.id]).filter(company__in = [req.user], ratingfield = "Resume").first()
        courseraCertificatesFeedback = Feedback.objects.all().filter(user__in = [profile.user.id]).filter(company__in = [req.user], ratingfield = "Coursera Certificates").first()
        profileFeedback = Feedback.objects.all().filter(user__in = [profile.user.id]).filter(company__in = [req.user], ratingfield = "Profile").first()
        skillsFeedback = Feedback.objects.all().filter(user__in = [profile.user.id]).filter(company__in = [req.user], ratingfield = "Skills").first()

        context["linkedInFeedback"] = linkedInFeedback
        context["resumeFeedback"] = resumeFeedback
        context["courseraCertificatesFeedback"] = courseraCertificatesFeedback
        context["profileFeedback"] = profileFeedback
        context["skillsFeedback"] = skillsFeedback
        if len(Feedback.objects.all().filter(user__in = [profile.user.id])):
            from utils import findAverageRating
            context['averageRating'] = findAverageRating(profile.user.id)
    return context


def profileEditController(req, profileId):
    from utils import profileCompleted, sendFormErrorMessages
    if req.method == "POST":
        from utils import tryExcept
        from home.models import UserProfile, CompanyProfile
        from home.forms import UpdateUserProfileForm

        profile = UserProfile.objects.get(id=profileId)
        if profile == None:
            profile = CompanyProfile.objects.get(id=profileId)
        user = profile.user
        username = user.username

        data = req.POST.dict()
        for key in data:
            tryExcept(req, user, key, data[key])
        user.save()
        data['user'] = user
        if user.userprofile.isUser:
            form = UpdateUserProfileForm(data, req.FILES, instance = profile)
            if form.is_valid():
                form.save()
                messages.success(req, f"Profile updated for {username}!")
                context = {"status": True}
                return context
            sendFormErrorMessages(req, form)
            context = {"status": False}
            return context
        else:
            user.companyprofile.email = data['email']
            user.companyprofile.name = data['name']
            user.companyprofile.contact_num = data['contact_num']
            user.companyprofile.number_of_employees = data['number_of_employees']
            user.companyprofile.website_link = data['website_link']
            user.companyprofile.save()
            messages.success(req, f"Profile updated for {username}!")
            context = {"status": True}
            return context

    context = {"status": True, "user": req.user}
    if not profileCompleted(req):
        context['showNav'] = False
    return context

def jobPostingController(req, jobPostingId):
    from home.models import JobPosting, UserProfile
    from utils import findAverageRating, sendFormErrorMessages

    jobposting = JobPosting.objects.get(id = jobPostingId)
    users = UserProfile.objects.all().filter(isUser = True)
    users_accepted = list(jobposting.users_accepted.all())
    willing_to_hire_users = list(jobposting.willing_to_hire.all())
    willing_to_hire_users = [user.userprofile for user in willing_to_hire_users]
    rem_users = [user for user in users if user not in willing_to_hire_users]

    users_accepted = [(user, findAverageRating(user.id)) for user in users_accepted]
    willing_to_hire_users = [(user, findAverageRating(user.id)) for user in willing_to_hire_users]
    rem_users = [(user, findAverageRating(user.id)) for user in rem_users]

    variables = req.POST.dict()
    if 'skills' in variables.keys():
        filterskills = req.POST.getlist('skills')
        filterskills = [int(_) for _ in filterskills]
        filterBy = variables.get('filterBy')

        filtered_rem_users = []
        print(filterskills)
        for user in rem_users:
            user_skills = list(user[0].skills.all())
            user_skills = [skill.id for skill in user_skills]
            if filterBy == 'or':
                print(user_skills)
                if any(item in user_skills for item in filterskills):
                    filtered_rem_users.append(user)
            else:
                if all(item in user_skills for item in filterskills):
                    filtered_rem_users.append(user)

        rem_users = filtered_rem_users

    context = {"status": True, "users_accepted":users_accepted, "jobPosting": jobposting, "willing_to_hire_users": willing_to_hire_users, 'rem_users': rem_users}
    return context

def createJobPostingController(req):
    from utils import sendFormErrorMessages
    from home.forms import CreateJobPostingForm

    if req.method == "POST":
        data = req.POST.dict()
        domain_skills = req.POST.getlist('domain_skills')
        requirement_skills = req.POST.getlist('requirement_skills')
        data['domain_skills'] = domain_skills
        data['requirement_skills'] = requirement_skills
        data['company'] = req.user
        form = CreateJobPostingForm(data, req.FILES)
        if form.is_valid():
            jobposting = form.save()
            req.user.companyprofile.jobpostings.add(jobposting)
            messages.success(req, f"JobPosting created successfully!")
            context = {"status": True, 'jobPostingId': jobposting.pk}
            return context

        sendFormErrorMessages(req, form)
        context = {"status": False, "jobPostingForm": CreateJobPostingForm()}
        return context
    context = {"status": True, "jobPostingForm": CreateJobPostingForm()}
    return context

def editJobPostingController(req, jobPostingId):
    from home.models import JobPosting
    from home.forms import EditJobPostingForm
    from utils import sendFormErrorMessages

    jobPosting = JobPosting.objects.get(id = jobPostingId)
    if req.method == "POST":
        data = req.POST.dict()
        domain_skills = req.POST.getlist('domain_skills')
        requirement_skills = req.POST.getlist('requirement_skills')
        data['domain_skills'] = domain_skills
        data['requirement_skills'] = requirement_skills
        data['company'] = req.user

        form = EditJobPostingForm(data, req.FILES, instance = jobPosting)
        if form.is_valid():
            form.save()

            messages.success(req, f"JobPosting successfully updated!")
            context = {"status": True}
            return context
        sendFormErrorMessages(req, form)
        context = {"status": False}
        return context

    context = {"status": True, "jobPostingForm": EditJobPostingForm(instance = jobPosting)}
    return context

def giveFeedbackController(req, companyId, userId):
    pass

def acceptController(req, jobPostingId, userId):
    from home.models import JobPosting
    from django.contrib.auth.models import User
    from utils import sendNotification

    user = User.objects.get(id = userId)
    jobposting = JobPosting.objects.get(id = jobPostingId)
    jobposting.willing_to_hire.add(user)
    jobposting.save()

    sendNotification(jobposting, user, "Want this job?")

def rejectController(req, jobPostingId, userId):
    from home.models import JobPosting
    from django.contrib.auth.models import User
    from utils import sendNotification

    user = User.objects.get(id = userId)
    jobposting = JobPosting.objects.get(id = jobPostingId)
    jobposting.willing_to_hire.remove(user)
    jobposting.save()

    sendNotification(jobposting, user, "Want this job?")

def rateUserController(req, userId, rating, feedbackField):
    from home.models import Feedback
    from django.contrib.auth.models import User
    from utils import sendReviewNotification
    user = User.objects.get(id = userId)
    company = req.user

    old_feedback = Feedback.objects.all().filter(user__in = [userId]).filter(company__in = [req.user.id]).filter(ratingfield = feedbackField).first()
    if old_feedback == None:
        feedback = Feedback(rating = rating, ratingfield = feedbackField)
        feedback.save()
        feedback.user.add(user)
        feedback.company.add(company)
        feedback.save()
        sendReviewNotification(req.user, user, "Reviewed", feedback)
    else:
        old_feedback.rating = rating
        old_feedback.save()
        sendReviewNotification(req.user, user, "Reviewed", old_feedback)
    context = {"status": True}
    return context