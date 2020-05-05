from flask import Blueprint

auth_view= Blueprint('auth_view',__name__)

# Profile view and settings

@auth_view.route("/dashboard",methods=['GET','POST'])
def profile():
    if current_user.is_authenticated:
        current_user_email = current_user.email

        all_snippets =[]
        # TODO better search algorithm find out
        if 'search'  not in request.args:
            all_snippets=Snippet.query.filter_by(email=current_user_email).all()

        else:
            search_query = request.args['search']
            all_snippets_temp=Snippet.query.filter_by(email=current_user_email).all()
            for snippet in all_snippets_temp:
                if search_query in snippet.name:
                    print(snippet.name)
                    all_snippets.append(snippet)

        if len(all_snippets) is None or len(all_snippets) is 0:
            return render_template("dashboard.html", empty=True, length=0, snippets=[0])

        title_array = []
        description_array = []
        id_array = []

        for snippet in all_snippets:
            title_array.append(snippet.name)
            description_array.append(snippet.description)
            id_array.append(snippet.id)
        return render_template("dashboard.html", 
                                length=len(title_array),
                                id_array=id_array,
                                name_array=title_array, 
                                description_array=description_array)

    else:
        return redirect(url_for('login'))

@auth_view.route('/settings',methods=['GET','POST'])
def settings():
    # TODO remove post if not necessary
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('settings.html',current_user_name=current_user.username)