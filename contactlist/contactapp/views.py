
from .forms import ContactBookForm
from .models import Group, ContactBook
from .forms import CustomUserCreationForm,RemoveMembersForm,AddMembersToGroupForm

# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy





def index(request):
    
    contacts = ContactBook.objects.all()
    search_input = request.GET.get('search-area')
    relationship_filter = request.GET.get('relationship-filter')

    if search_input:
        contacts = contacts.filter(full_name__icontains=search_input)

    if relationship_filter:
        if relationship_filter.isdigit():
            contacts = contacts.filter(id=relationship_filter)
        else:
           contacts = contacts.filter(relationship__rel=relationship_filter)

    
    contacts = contacts.order_by('full_name')

    initials = [contact.full_name[0].upper() for contact in contacts if contact.full_name]
    contact_starting_letters = set(contact.full_name[0].upper() for contact in contacts if contact.full_name)
    contact_starting_letters = sorted(list(contact_starting_letters))

    relationships = ContactBook.objects.values_list('relationship', flat=True).distinct()
    alphabets = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

    contacts_by_alphabet = {letter: [] for letter in alphabets}

    for contact in contacts:
        first_letter = contact.full_name[0].upper() if contact.full_name else '#'
        contacts_by_alphabet[first_letter].append(contact)
    

    return render(request, 'index.html', {'contacts': contacts, 'search_input': search_input, 'relationship_filter': relationship_filter, 'relationships': relationships,'initials': sorted(set(initials)),'alphabets': alphabets,'contacts_by_alphabet':contacts_by_alphabet,'contact_starting_letters':contact_starting_letters})

def addContact(request):
    
    if request.method == 'POST':
        new_contact= ContactBookForm(request.POST,request.FILES)
        if new_contact.is_valid():
            new_contact1 = new_contact.save(commit=False)
            new_contact1.user = request.user
            new_contact1.save()
            return redirect('index')
        else:
            print(new_contact.errors)
    else:
        new_contact = ContactBookForm()

    return render(request, 'new.html', {'new_contact': new_contact})
def editContact(request, pk):
    contact = ContactBook.objects.get(id=pk)
    

    if request.method == 'POST':
        form = ContactBookForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
        return redirect('/profile/'+str(contact.id))
    else:
        form = ContactBookForm(instance=contact)
    return render(request, 'edit.html', {'form':form,'contact': contact})


def contactProfile(request, pk):
    contact = ContactBook.objects.get(id=pk)
    return render(request, 'contact-profile.html', {'contact':contact})


def deleteContact(request, pk):
    contact = ContactBook.objects.get(id=pk)

    #if request.method == 'POST':
    contact.delete()
    return redirect('index')

    #return render(request, 'index.html', {'contact': contact})


def add_favorites(request):
    contacts = ContactBook.objects.exclude(is_favorite=True)
    search_input = request.GET.get('search-area')

    if search_input:
        contacts = contacts.filter(full_name__icontains=search_input)
    return render(request, 'add_favorites.html', {'contacts': contacts,'search_input':search_input})



def add_to_favorites(request, contact_id):
    contact = ContactBook.objects.get(id=contact_id)
    contact.is_favorite = True
    contact.save()
    return redirect('add-favorites')  
   

def remove_from_favorites(request, contact_id):
    contact = ContactBook.objects.get(id=contact_id)
    contact.is_favorite = False
    contact.save()
    return redirect('view-favourites')
    

def view_favourites(request):
    favourites = ContactBook.objects.filter(is_favorite=True)
    search_input = request.GET.get('search-area')
    if search_input:
        favourites = favourites.filter(full_name__icontains=search_input)
    return render(request, 'view_favourites.html', {'favourites': favourites,'search_input':search_input})


def create_group(request):
    contacts = ContactBook.objects.all()
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        selected_contacts_ids = request.POST.getlist('selected_contacts')
        group = Group.objects.create(name=group_name)
        selected_contacts = ContactBook.objects.filter(id__in=selected_contacts_ids)
        group.members.set(selected_contacts)
    return render(request, 'create_group.html', {'contacts': contacts})


def add_members_to_group(request, group_id):
    group = Group.objects.get(id=group_id)
    contacts = ContactBook.objects.all()  
    if request.method == 'POST':
        selected_contacts_ids = request.POST.getlist('selected_contacts')
        selected_contacts = ContactBook.objects.filter(id__in=selected_contacts_ids)
        group.members.add(*selected_contacts)
        return redirect('create_group')
    return render(request, 'add_members_to_group.html', {'group': group, 'contacts': contacts})

    

def view_groups(request):
    groups = Group.objects.all()
    group_data = []
    for group in groups:
        group_members = group.members.all()
        group_data.append({'group': group, 'members': group_members})

    return render(request, 'view_groups.html', {'group_data': group_data})


def save_group(request, group_id):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        selected_contacts_ids = request.POST.getlist('selected_contacts')
        selected_contacts = ContactBook.objects.filter(id__in=selected_contacts_ids)
        
        if group_id:
            group = Group.objects.get(id=group_id)
            group.name = group_name
            group.save()
            group.members.set(selected_contacts)
        else:
            group = Group.objects.create(name=group_name)
            group.members.set(selected_contacts)

        return redirect('view_group', group_id=group.id)

    return redirect('index')


def loginView(request):
    authenticationForm = AuthenticationForm()
    if request.method=="POST":
        authenticationForm = AuthenticationForm(request, data=request.POST or None)
        if authenticationForm.is_valid():
            username = authenticationForm.cleaned_data["username"]
            password = authenticationForm.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user=user)
                return redirect("index")
        else:
            print(authenticationForm.errors)

    return render(request, template_name="login.html", context={"authenticationForm" : authenticationForm})


def registration(request):
    user_creation_form = CustomUserCreationForm()  
    if request.method == "POST":
        user_creation_form = CustomUserCreationForm(request.POST or None)
        if user_creation_form.is_valid():
            username = user_creation_form.cleaned_data["username"]
            password = user_creation_form.cleaned_data["password1"]
            user_creation_form = user_creation_form.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user=user)
                return redirect("login")
    else:
        print(user_creation_form.errors)
    return render(request, template_name="registration.html", context={"UserCreationForm": user_creation_form})


def view_group(request, group_id):
    group = Group.objects.get(id=group_id)

    if request.method == 'POST':
        add_members_form = AddMembersToGroupForm(request.POST)
        if add_members_form.is_valid():
            selected_members_ids = add_members_form.cleaned_data.get('selected_members')
            selected_members = ContactBook.objects.filter(id__in=selected_members_ids)
            group.members.add(*selected_members)
            return redirect('view_group', group_id=group_id)
    else:
        add_members_form = AddMembersToGroupForm()

    if request.method == 'POST':
        remove_members_form = RemoveMembersForm(request.POST)
        if remove_members_form.is_valid():
            selected_members_ids = remove_members_form.cleaned_data.get('selected_members')
            selected_members = ContactBook.objects.filter(id__in=selected_members_ids)
            group.members.remove(*selected_members)

            return redirect('view_group', group_id=group_id)
    else:
        remove_members_form = RemoveMembersForm()

    return render(request, 'view_group.html', {'group': group, 'remove_members_form': remove_members_form,'add_members_form':add_members_form})


def logout(request):
    
    return LogoutView.as_view(next_page=reverse_lazy('loginView'))(request)