from flask import Blueprint, flash, render_template, request, redirect, url_for

from webapp.prefix.forms import PrefixForm
from webapp.prefix.models import db, Prefix

blueprint = Blueprint('prefix', __name__, url_prefix='/prefixes')


@blueprint.route('/<int:prefix_id>', methods=['POST', 'GET'])
def prefix_view(prefix_id):
    prefix = Prefix.query.get(prefix_id)
    prefix_form = PrefixForm(obj=prefix)
    if request.method == 'POST':
        prefix_form = PrefixForm()
        if prefix_form.validate_on_submit():
            prefix.prefix = prefix_form.prefix.data
            db.session.add(prefix)
            db.session.commit()
            flash('Successfully updated')
            return redirect(url_for('prefix.prefix_view', prefix_id=prefix.id))

    return render_template('prefix/prefix.html', form=prefix_form, prefix=prefix)
