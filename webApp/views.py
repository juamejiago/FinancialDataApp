from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .forms import CreateTag, CustomUserCreationForm
from .models import Tag, Category, Profile
from .yahoo_query import financial_analysis as fn
import json
import ast
import datetime


# Create your views here.
def tag_ordering(request):
    if request.method == "POST":
        filter_selected = json.loads(request.body)
        columns = [
            "symbol",
            "shortName",
            "debt/Equ",
            "%Insiders",
            "Price",
            "t.Price",
            "Upside",
            "t.PE",
            "f.PE",
            "t.Eps",
            "f.Eps",
            "ROA",
            "ROE",
            "profit.M",
            "Myscore",
            "Mycount",
        ]
        index_filter = columns.index(filter_selected[0:-1])
        if filter_selected[-1] == "s":
            for i in range(0, len(Auxiliar_class.auxiliar_table)):
                for j in range(i + 1, len(Auxiliar_class.auxiliar_table)):
                    if (
                        Auxiliar_class.auxiliar_table[j][index_filter]
                        > Auxiliar_class.auxiliar_table[i][index_filter]
                    ):
                        (
                            Auxiliar_class.auxiliar_table[i],
                            Auxiliar_class.auxiliar_table[j],
                        ) = (
                            Auxiliar_class.auxiliar_table[j],
                            Auxiliar_class.auxiliar_table[i],
                        )

        elif filter_selected[-1] == "i":
            for i in range(0, len(Auxiliar_class.auxiliar_table)):
                for j in range(i + 1, len(Auxiliar_class.auxiliar_table)):
                    if (
                        Auxiliar_class.auxiliar_table[j][index_filter]
                        < Auxiliar_class.auxiliar_table[i][index_filter]
                    ):
                        (
                            Auxiliar_class.auxiliar_table[i],
                            Auxiliar_class.auxiliar_table[j],
                        ) = (
                            Auxiliar_class.auxiliar_table[j],
                            Auxiliar_class.auxiliar_table[i],
                        )

    return redirect("home", permanent=True)


def delete_tag(request):
    Auxiliar_class.selected_profile = Database_handler.consult_selected_profile(request)
    if request.method == "POST":
        tag_symbols = json.loads(request.body)
        for tag_symbol in tag_symbols:
            tag_already_saved_profile = (
                Auxiliar_class.check_tag_already_saved_in_selected_profile(
                    tag_symbol, Auxiliar_class.selected_profile
                )
            )
            if tag_already_saved_profile:
                tag_selected = Database_handler.consult_tag_by_filter(tag_symbol)[0]
                Database_handler.remove_tag_to_profile(
                    tag_selected, Auxiliar_class.selected_profile
                )
        tags_database_data = list(
            Auxiliar_class.selected_profile.associated_tags.all().values_list()
        )
        if len(tags_database_data) == 0:
            Database_handler.delete_data_from_database(
                Database_handler.consult_all_categories_saved()
            )
        Auxiliar_class.auxiliar_table = tags_database_data

    return redirect("home", permanent=True)


@login_required
def delete_category(request):
    if request.method == "POST":
        category = json.loads(request.body)
        Database_handler.remove_category_to_profile(
            Database_handler.consult_category_by_filter(category)[0],
            Auxiliar_class.selected_profile,
        )
        Database_handler.delete_data_from_database(
            Database_handler.consult_category_by_filter(category)
        )
        if Auxiliar_class.category_selected == category:
            selected_profile = Database_handler.consult_selected_profile(request)
            Auxiliar_class.selected_profile = selected_profile
            tags_database_data = list(
                selected_profile.associated_tags.all().values_list()
            )
            Auxiliar_class.auxiliar_table = tags_database_data
            Auxiliar_class.category_selected = "visualize_all_tags"

    return redirect("home", permanent=True)


@login_required
def delete_tag_from_category(request):
    if request.method == "POST":
        tag_symbols = json.loads(request.body)
        selected_category = Auxiliar_class.category_selected
        Database_handler.update_category_data(selected_category, tag_symbols, "delete")
        selected_category_data = Database_handler.consult_category_by_filter(
            Auxiliar_class.category_selected
        ).values_list()
        selected_tags_string = selected_category_data[0][1]
        selected_tags = ast.literal_eval(selected_tags_string)
        tags_database_data = list(
            Database_handler.consult_tags_according_to_filter(
                selected_tags
            ).values_list()
        )
        if len(tags_database_data) == 0:
            selected_profile = Database_handler.consult_selected_profile(request)
            Auxiliar_class.selected_profile = selected_profile
            tags_database_data = list(
                selected_profile.associated_tags.all().values_list()
            )
            Auxiliar_class.auxiliar_table = tags_database_data
            Database_handler.delete_data_from_database(
                Database_handler.consult_category_by_filter(selected_category)
            )
            Auxiliar_class.category_selected = "visualize_all_tags"

        Auxiliar_class.auxiliar_table = tags_database_data

    return redirect("home", permanent=True)


@login_required
def add_tag_to_category(request):
    tags_database_data = Auxiliar_class.auxiliar_table
    name_categories = Auxiliar_class.obtain_name_categories()

    if request.method == "POST":
        category_tags_selected = json.loads(request.body)
        selected_categories = category_tags_selected["selected_categories"]
        selected_tags = category_tags_selected["selected_tags"]
        for category in selected_categories:
            for tag in selected_tags:
                Database_handler.update_category_data(category, tag, "add")

        return redirect("home", permanent=True)
    elif request.method == "GET":
        return render(
            request,
            "select_category.html",
            {
                "headers_title_list": [
                    "symbol",
                    "shortName",
                    "debt/Equ",
                    "%Insiders",
                    "Price",
                    "t.Price",
                    "Upside",
                    "t.PE",
                    "f.PE",
                    "t.Eps",
                    "f.Eps",
                    "ROA",
                    "ROE",
                    "profit.M",
                    "Myscore",
                    "Mycount",
                ],
                "financial_data_tags": tags_database_data,
                "len_tags": len(tags_database_data),
                "comprobation_create_tag": True,
                "list_categories": name_categories,
                "mode": "add",
                "current_category": Auxiliar_class.category_selected,
                "len_categories": len(name_categories),
                "current_year": datetime.datetime.now().year,
            },
        )


@login_required
def transfer_tag_between_categories(request):
    tags_database_data = Auxiliar_class.auxiliar_table

    name_categories = Auxiliar_class.obtain_name_categories()

    if request.method == "POST":
        category_tags_selected = json.loads(request.body)
        selected_categories = category_tags_selected["selected_categories"]
        selected_tags = category_tags_selected["selected_tags"]
        for category in selected_categories:
            for tag in selected_tags:
                Database_handler.update_category_data(category, tag, "add")
        Database_handler.update_category_data(
            Auxiliar_class.category_selected, selected_tags, "delete"
        )

        return visualize_category(request, Auxiliar_class.category_selected)

    elif request.method == "GET":
        return render(
            request,
            "select_category.html",
            {
                "headers_title_list": [
                    "symbol",
                    "shortName",
                    "debt/Equ",
                    "%Insiders",
                    "Price",
                    "t.Price",
                    "Upside",
                    "t.PE",
                    "f.PE",
                    "t.Eps",
                    "f.Eps",
                    "ROA",
                    "ROE",
                    "profit.M",
                    "Myscore",
                    "Mycount",
                ],
                "financial_data_tags": tags_database_data,
                "len_tags": len(tags_database_data),
                "comprobation_create_tag": True,
                "list_categories": name_categories,
                "mode": "transfer",
                "current_category": Auxiliar_class.category_selected,
                "len_categories": len(name_categories),
                "current_year": datetime.datetime.now().year,
            },
        )


def create_tag(request):
    inserted_symbol = str(request.POST.get("symbol"))
    form_symbol = CreateTag(request.POST)
    tags_database_data = Auxiliar_class.auxiliar_table
    Auxiliar_class.selected_profile = Database_handler.consult_selected_profile(request)

    if (
        inserted_symbol is None
        or inserted_symbol == "Bad format or it already exists. Try again"
    ):
        inserted_symbol = ""
    inserted_symbol = inserted_symbol.upper()

    if request.method == "POST":
        name_categories = Auxiliar_class.obtain_name_categories()

        if (
            len(inserted_symbol) == inserted_symbol.count(" ")
            or inserted_symbol.count(" ") > len(inserted_symbol) // 2
        ):
            initial_data = {"symbol": "Bad format or it already exists. Try again"}
            return render(
                request,
                "create_tag.html",
                {
                    "form": CreateTag(initial=initial_data),
                    "headers_title_list": [
                        "symbol",
                        "shortName",
                        "debt/Equ",
                        "%Insiders",
                        "Price",
                        "t.Price",
                        "Upside",
                        "t.PE",
                        "f.PE",
                        "t.Eps",
                        "f.Eps",
                        "ROA",
                        "ROE",
                        "profit.M",
                        "Myscore",
                        "Mycount",
                    ],
                    "financial_data_tags": tags_database_data,
                    "len_tags": len(tags_database_data),
                    "comprobation_create_tag": True,
                    "current_category": Auxiliar_class.category_selected,
                    "list_categories": name_categories,
                    "category": Auxiliar_class.category_selected,
                    "len_categories": len(name_categories),
                    "current_year": datetime.datetime.now().year,
                },
            )
        # Implements a series of comprobations if the inserted text at the forms is shorter than 7 characters
        elif len(inserted_symbol) <= 6:
            initial_data = None
            tag_already_saved = False
            # Checks that that the inserted tag symbol is not saved on the database
            tag_already_saved = Auxiliar_class.check_tag_already_saved_in_general_db(
                inserted_symbol
            )
            tag_already_saved_profile = (
                Auxiliar_class.check_tag_already_saved_in_selected_profile(
                    inserted_symbol, Auxiliar_class.selected_profile
                )
            )
            if not (tag_already_saved) and form_symbol.is_valid():
                # Create a new tag and save it to the database
                row_with_data = fn.financeAnalisis(inserted_symbol)
                Database_handler.create_new_tag(row_with_data)
            if not (tag_already_saved_profile) and form_symbol.is_valid():
                selected_tag = Database_handler.consult_tag_by_filter(inserted_symbol)[
                    0
                ]
                Database_handler.add_tag_to_profile(
                    selected_tag, Auxiliar_class.selected_profile
                )
            else:
                initial_data = {"symbol": "Bad format or it already exists. Try again"}
            if Auxiliar_class.category_selected == "visualize_all_tags":
                selected_profile = Database_handler.consult_selected_profile(request)
                Auxiliar_class.selected_profile = selected_profile
                tags_database_data = list(
                    selected_profile.associated_tags.all().values_list()
                )
                Auxiliar_class.auxiliar_table = tags_database_data
            else:
                Database_handler.update_category_data(
                    Auxiliar_class.category_selected, inserted_symbol, "add"
                )
                selected_category_data = Database_handler.consult_category_by_filter(
                    Auxiliar_class.category_selected
                ).values_list()
                selected_tags_string = selected_category_data[0][1]
                selected_tags = ast.literal_eval(selected_tags_string)
                tags_database_data = list(
                    Database_handler.consult_tags_according_to_filter(
                        selected_tags
                    ).values_list()
                )
                Auxiliar_class.auxiliar_table = tags_database_data
            return render(
                request,
                "create_tag.html",
                {
                    "form": CreateTag(initial=initial_data),
                    "headers_title_list": [
                        "symbol",
                        "shortName",
                        "debt/Equ",
                        "%Insiders",
                        "Price",
                        "t.Price",
                        "Upside",
                        "t.PE",
                        "f.PE",
                        "t.Eps",
                        "f.Eps",
                        "ROA",
                        "ROE",
                        "profit.M",
                        "Myscore",
                        "Mycount",
                    ],
                    "financial_data_tags": tags_database_data,
                    "len_tags": len(tags_database_data),
                    "comprobation_create_tag": False,
                    "current_category": Auxiliar_class.category_selected,
                    "list_categories": name_categories,
                    "category": Auxiliar_class.category_selected,
                    "len_categories": len(name_categories),
                    "current_year": datetime.datetime.now().year,
                },
            )

        # Implements a loop routine if the inserted text at the forms is larger than 6 characters
        elif len(inserted_symbol) > 6:
            names_unfixed = list(inserted_symbol)
            names_fixed = []
            if names_unfixed[-1] != ",":
                names_unfixed.append(",")
            while True:
                for w in names_unfixed:
                    # Looks for the comma as this is the separation between diferents tag symbols
                    if w == ",":
                        tag_already_saved = False
                        index = names_unfixed.index(w)
                        names_fixed = names_unfixed[0:index]
                        del names_unfixed[0 : index + 2]
                        # First comprobation on all tags on the database
                        tag_already_saved = (
                            Auxiliar_class.check_tag_already_saved_in_general_db(
                                "".join(names_fixed)
                            )
                        )
                        tag_already_saved_profile = (
                            Auxiliar_class.check_tag_already_saved_in_selected_profile(
                                "".join(names_fixed), Auxiliar_class.selected_profile
                            )
                        )

                        if names_fixed.count(" ") != len(names_fixed):
                            if not (tag_already_saved):
                                row_with_data = fn.financeAnalisis("".join(names_fixed))
                                Database_handler.create_new_tag(row_with_data)
                            if not (tag_already_saved_profile):
                                selected_tag = Database_handler.consult_tag_by_filter(
                                    "".join(names_fixed)
                                )[0]
                                Database_handler.add_tag_to_profile(
                                    selected_tag, Auxiliar_class.selected_profile
                                )
                            if Auxiliar_class.category_selected != "visualize_all_tags":
                                selected_category_data = (
                                    Database_handler.consult_category_by_filter(
                                        Auxiliar_class.category_selected
                                    ).values_list()
                                )
                                selected_tags_string = selected_category_data[0][1]
                                selected_tags = ast.literal_eval(selected_tags_string)
                                tags_database_data = list(
                                    Database_handler.consult_tags_according_to_filter(
                                        selected_tags
                                    ).values_list()
                                )
                            else:
                                tags_database_data = list(
                                    Database_handler.consult_all_tags_saved().values_list()
                                )
                            # Second comprobation on all tags on the category
                            tag_already_saved = False
                            if Auxiliar_class.category_selected != "visualize_all_tags":
                                for saved_tags in tags_database_data:
                                    if (
                                        "".join(names_fixed)
                                        == str(saved_tags[0]).upper()
                                    ):
                                        tag_already_saved = True
                                        break
                                if not (tag_already_saved):
                                    Database_handler.update_category_data(
                                        Auxiliar_class.category_selected,
                                        "".join(names_fixed),
                                        "add",
                                    )
                                selected_category_data = (
                                    Database_handler.consult_category_by_filter(
                                        Auxiliar_class.category_selected
                                    ).values_list()
                                )
                                selected_tags_string = selected_category_data[0][1]
                                selected_tags = ast.literal_eval(selected_tags_string)
                                tags_database_data = list(
                                    Database_handler.consult_tags_according_to_filter(
                                        selected_tags
                                    ).values_list()
                                )
                        names_fixed = []
                # Exits the while loop when the list is already passed
                if len(names_unfixed) == 0:
                    break
            Auxiliar_class.auxiliar_table = tags_database_data

        return redirect("/create_tag/")

    else:
        if Auxiliar_class.category_selected == "visualize_all_tags":
            selected_profile = Database_handler.consult_selected_profile(request)
            Auxiliar_class.selected_profile = selected_profile
            tags_database_data = list(
                selected_profile.associated_tags.all().values_list()
            )
            Auxiliar_class.auxiliar_table = tags_database_data
        else:
            tags_database_data = Auxiliar_class.auxiliar_table

        name_categories = Auxiliar_class.obtain_name_categories()

        return render(
            request,
            "create_tag.html",
            {
                "form": CreateTag(),
                "headers_title_list": [
                    "symbol",
                    "shortName",
                    "debt/Equ",
                    "%Insiders",
                    "Price",
                    "t.Price",
                    "Upside",
                    "t.PE",
                    "f.PE",
                    "t.Eps",
                    "f.Eps",
                    "ROA",
                    "ROE",
                    "profit.M",
                    "Myscore",
                    "Mycount",
                ],
                "financial_data_tags": tags_database_data,
                "len_tags": len(tags_database_data),
                "comprobation_create_tag": False,
                "current_category": Auxiliar_class.category_selected,
                "list_categories": name_categories,
                "category": Auxiliar_class.category_selected,
                "len_categories": len(name_categories),
                "current_year": datetime.datetime.now().year,
            },
        )


def home(request):
    name_categories = Auxiliar_class.obtain_name_categories()
    if Auxiliar_class.category_selected == "":
        Auxiliar_class.category_selected = "visualize_all_tags"
    if request.user.is_authenticated:
        if request.method == "POST":
            selected_category = json.loads(request.body)
            category = selected_category[0]
            if (
                len(Database_handler.consult_category_by_filter(category).values_list())
                == 0
            ):
                Auxiliar_class.category_selected = category
                Database_handler.create_new_category(selected_category)
                Database_handler.add_category_to_profile(
                    Database_handler.consult_category_by_filter(category)[0],
                    Auxiliar_class.selected_profile,
                )
                selected_category_data = Database_handler.consult_category_by_filter(
                    category
                ).values_list()
                selected_tags_string = selected_category_data[0][1]
                selected_tags = ast.literal_eval(selected_tags_string)
                tags_database_data = list(
                    Database_handler.consult_tags_according_to_filter(
                        selected_tags
                    ).values_list()
                )
                Auxiliar_class.auxiliar_table = tags_database_data
        if Auxiliar_class.category_selected == "visualize_all_tags":
            selected_profile = Database_handler.consult_selected_profile(request)
            Auxiliar_class.selected_profile = selected_profile
            tags_database_data = list(
                selected_profile.associated_tags.all().values_list()
            )
            if len(Auxiliar_class.auxiliar_table) == 0:
                Auxiliar_class.auxiliar_table = tags_database_data
            else:
                tags_database_data = Auxiliar_class.auxiliar_table
        else:
            tags_database_data = Auxiliar_class.auxiliar_table
    else:
        profile_objects = list(Database_handler.consult_all_profiles_saved())
        tags_database_data = list(
            profile_objects[-1].associated_tags.all().values_list()
        )
        if len(Auxiliar_class.auxiliar_table) == 0:
            Auxiliar_class.auxiliar_table = tags_database_data
        else:
            tags_database_data = Auxiliar_class.auxiliar_table
    return render(
        request,
        "home.html",
        {
            "headers_title_list": [
                "symbol",
                "shortName",
                "debt/Equ",
                "%Insiders",
                "Price",
                "t.Price",
                "Upside",
                "t.PE",
                "f.PE",
                "t.Eps",
                "f.Eps",
                "ROA",
                "ROE",
                "profit.M",
                "Myscore",
                "Mycount",
            ],
            "financial_data_tags": tags_database_data,
            "len_tags": len(tags_database_data),
            "list_categories": name_categories,
            "current_category": Auxiliar_class.category_selected,
            "len_categories": len(name_categories),
            "current_year": datetime.datetime.now().year,
        },
    )


def presentation(request):
    return render(
        request, "presentation.html", {"current_year": datetime.datetime.now().year}
    )


@login_required
def login(request):
    messages.success(request, "Successful login. Welcome again!")
    return redirect("home")


@login_required
def exit(request):
    Auxiliar_class.auxiliar_table = []
    Auxiliar_class.category_selected = ""
    Auxiliar_class.selected_profile = ""
    logout(request)
    messages.success(request, "Successful logout. Hope to see you again soon!")
    return redirect("presentation")


def register(request):
    data = {
        "form": CustomUserCreationForm(),
        "current_year": datetime.datetime.now().year,
    }
    if request.method == "POST":
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            messages.success(request, "Successful registration!")
            return redirect(to="login")
        else:
            data["form"] = user_creation_form
            return render(request, "registration/register.html", data)
    else:
        return render(request, "registration/register.html", data)


@login_required
def visualize_category(request, selected_category=None):
    if selected_category == None:
        selected_category = json.loads(request.body)

    tags_database_data = []
    Auxiliar_class.category_selected = selected_category
    if selected_category == "visualize_all_tags":
        selected_profile = Database_handler.consult_selected_profile(request)
        Auxiliar_class.selected_profile = selected_profile
        tags_database_data = list(selected_profile.associated_tags.all().values_list())
        Auxiliar_class.auxiliar_table = tags_database_data
    else:
        selected_category_data = Database_handler.consult_category_by_filter(
            selected_category
        ).values_list()
        selected_tags_string = selected_category_data[0][1]
        selected_tags = ast.literal_eval(selected_tags_string)
        tags_database_data = list(
            Database_handler.consult_tags_according_to_filter(
                selected_tags
            ).values_list()
        )
    Auxiliar_class.auxiliar_table = tags_database_data
    return redirect("home", permanent=True)


def update_tag(request):
    Database_handler.update_tags_data()
    Auxiliar_class.auxiliar_table = []
    if request.method == "POST":
        response = {
            "message": "OK",
        }
        return JsonResponse(response)
    else:
        return redirect("home")


class Auxiliar_class:
    auxiliar_table = []
    category_selected = ""
    selected_profile = None

    @classmethod
    def obtain_name_categories(cls):
        categories_database_data = list(
            Database_handler.consult_all_categories_saved().values_list()
        )
        name_categories = []
        for category_tuple in categories_database_data:
            name_categories.append(category_tuple[0])
        return name_categories

    @classmethod
    def check_tag_already_saved_in_general_db(cls, inserted_symbol):
        tag_already_saved = False
        tags_database_data = list(
            Database_handler.consult_all_tags_saved().values_list()
        )
        for saved_tags in tags_database_data:
            if inserted_symbol in str(saved_tags[0]).upper():
                tag_already_saved = True
                break
        return tag_already_saved

    @classmethod
    def check_tag_already_saved_in_selected_profile(
        cls, inserted_symbol, selected_profile
    ):
        tag_already_saved = False
        tags_database_data = list(selected_profile.associated_tags.all().values_list())
        for saved_tags in tags_database_data:
            if inserted_symbol in str(saved_tags[0]).upper():
                tag_already_saved = True
                break
        return tag_already_saved


class Database_handler:
    @classmethod
    def consult_all_tags_saved(cls):
        return Tag.objects.all()

    @classmethod
    def consult_tags_according_to_filter(cls, filter):
        return Tag.objects.filter(symbol__in=filter)

    @classmethod
    def consult_selected_profile(cls, request):
        return Profile.objects.filter(user=request.user)[0]

    @classmethod
    def consult_all_profiles_saved(cls):
        return Profile.objects.all()

    @classmethod
    def consult_all_categories_saved(cls):
        return Category.objects.all()

    @classmethod
    def create_new_tag(cls, data_tag):
        Tag.objects.create(
            symbol=data_tag[0],
            short_name=data_tag[1],
            debt_equ=data_tag[2],
            insiders=data_tag[3],
            price=data_tag[4],
            t_price=data_tag[5],
            upside=data_tag[6],
            t_pe=data_tag[7],
            f_pe=data_tag[8],
            t_eps=data_tag[9],
            f_eps=data_tag[10],
            roa=data_tag[11],
            roe=data_tag[12],
            profit_m=data_tag[13],
            my_score=data_tag[14],
            my_count=data_tag[15],
        )

    @classmethod
    def add_tag_to_profile(cls, tag_to_add, selected_profile):
        selected_profile.associated_tags.add(tag_to_add)
        selected_profile.save()

    @classmethod
    def remove_tag_to_profile(cls, tag_to_delete, selected_profile):
        selected_profile.associated_tags.remove(tag_to_delete)
        selected_profile.save()

    @classmethod
    def create_new_category(cls, data_category):
        Category.objects.create(
            name=data_category[0], associated_tags=data_category[1:]
        )

    @classmethod
    def add_category_to_profile(cls, category_to_add, selected_profile):
        selected_profile.associated_categories.add(category_to_add)
        selected_profile.save()

    @classmethod
    def remove_category_to_profile(cls, category_to_delete, selected_profile):
        selected_profile.associated_categories.remove(category_to_delete)
        selected_profile.save()

    @classmethod
    def consult_tag_by_filter(cls, filter):
        return Tag.objects.filter(symbol=filter)

    @classmethod
    def consult_category_by_filter(cls, filter):
        return Category.objects.filter(name=filter)

    @classmethod
    def delete_data_from_database(cls, queryset):
        queryset.delete()

    @classmethod
    def update_tags_data(cls):
        all_tags = list(cls.consult_all_tags_saved())
        for tag in all_tags:
            new_data = fn.financeAnalisis(tag.symbol)
            i = 0
            for field_to_modify in tag._meta.fields:
                if field_to_modify.name != "symbol":
                    setattr(tag, field_to_modify.name, new_data[i])
                i += 1
            tag.save()

    @classmethod
    def update_category_data(cls, category, new_tags, mode):
        selected_category = cls.consult_category_by_filter(category)[0]
        if mode == "add":
            for field_to_modify in selected_category._meta.fields:
                if field_to_modify.name != "name":
                    tags_to_add = ast.literal_eval(selected_category.associated_tags)
                    if not (new_tags in tags_to_add):
                        tags_to_add.append(new_tags)
                        selected_category.associated_tags = tags_to_add
        elif mode == "delete":
            for field_to_modify in selected_category._meta.fields:
                if field_to_modify.name != "name":
                    current_tags = ast.literal_eval(selected_category.associated_tags)
                    for tag in new_tags:
                        if tag in current_tags:
                            current_tags.remove(tag)
                    tags_update = current_tags
                    selected_category.associated_tags = tags_update
        selected_category.save()
