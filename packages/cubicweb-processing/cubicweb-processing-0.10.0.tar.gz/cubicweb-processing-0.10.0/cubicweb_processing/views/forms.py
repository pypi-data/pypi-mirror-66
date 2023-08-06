# copyright 2012-2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-processing forms"""

from six import text_type

from logilab.mtconverter import xml_escape
from logilab.common.decorators import cachedproperty

from cubicweb import tags, _
from cubicweb.predicates import is_instance, match_kwargs, specified_etype_implements
from cubicweb.web import formwidgets
from cubicweb.web.form import FieldNotFound
from cubicweb.web.views import uicfg, autoform, formrenderers

from cubicweb_processing.views.predicates import has_link_to_runchain

_afs = uicfg.autoform_section
_affk = uicfg.autoform_field_kwargs
_afs.tag_subject_of(('*', 'parameter_of', '*'), 'main', 'hidden')
_afs.tag_object_of(('*', 'executable', 'Executable'), 'main', 'hidden')
_afs.tag_subject_of(('RunChain', 'uses_executable', 'Executable'), 'main', 'attributes')


class WiringForRunChainCreationForm(autoform.AutomaticEntityForm):
    __select__ = (autoform.AutomaticEntityForm.__select__ &
                  has_link_to_runchain())

    def editable_attributes(self, strict=False):
        res = super(WiringForRunChainCreationForm, self).editable_attributes(strict)
        return [(rtype, role) for rtype, role in res if rtype != 'name']


# Run form #####################################################################

# hide the executable and display values
_afs.tag_subject_of(('Run', 'executable', '*'), 'main', 'hidden')
_afs.tag_object_of(('*', 'value_of_run', 'Run'), 'main', 'inlined')
_afs.tag_subject_of(('*', 'value_of_run', '*'), 'main', 'hidden')
# ParameterValueFile subform config
_afs.tag_subject_of(('ParameterValueFile', 'value_file', '*'), 'main', 'inlined')
_afs.tag_attribute(('File', 'description'), 'inlined', 'hidden')
_afs.tag_attribute(('File', 'title'), 'inlined', 'hidden')

def value_file_label(form, field):
    return pdef(form).name
_affk.tag_subject_of(('ParameterValueFile', 'value_file', '*'),
                     {'label': value_file_label})


class RunEditForm(autoform.AutomaticEntityForm):
    """overriden from automatic form to display inlined forms according to the
    Run's executable parameter definitions instead of the schema. Rendering is
    also heavily customized so it looks almost like regular attributes of the
    run.
    """
    __select__ = autoform.AutomaticEntityForm.__select__ & is_instance('Run')

    _('creating Run (Run executable Executable %(linkto)s)')

    @cachedproperty
    def param_defs(self):
        """ Return the list of ParameterDefiniton(s) relevant for this run.

        This methods first looks for an Executable which will be
        linked to this Run (__linkto form attribute) then, if none, it
        checks if the Run has an executable relation (typically the
        case when editing entity).

        The methods returns [] when no Executable could be
        associated with the Run and [] when one with no
        ParametersDefinitions has been found.
        """
        exec_eids = self.linked_to.get( ('executable', 'subject') )
        if exec_eids is None:
            if self.edited_entity.executable:
                executable = self.edited_entity.exe
            else:
                return []
        else:
            assert len(exec_eids) == 1
            executable = self._cw.entity_from_eid(exec_eids[0])
        return [pdef for pdef in executable.reverse_parameter_of
                if pdef.param_type == 'input']

    def inlined_form_views(self):
        """compute and return list of inlined form views (hosting the inlined
        form object)
        """
        entity = self.edited_entity
        edition = entity.has_eid()
        rschema = self._cw.vreg.schema.rschema('value_of_run')
        role = 'object'
        for pdef in self.param_defs:
            # XXX filter out pdef whose value is specified by previous run
            ttype = 'ParameterValue' + pdef.value_type
            try:
                if edition:
                    formview = next(self.inline_edition_form_view(rschema, ttype, role))
                else:
                    formview = next(self.inline_creation_form_view(rschema, ttype, role))
            except StopIteration:
                continue
            form = formview.form
            try:
                pdef_field = form.field_by_name('param_def', 'subject')
            except FieldNotFound:
                pass
            else:
                # meaning that the user does not have the permission to edit
                # param_def relations
                pdef_field.init_widget(formwidgets.HiddenInput)
                pdef_field.value = text_type(pdef.eid)
            yield formview


# Run form rendering customization: fasten your seat belt ######################

class ParameterValueFileEditForm(autoform.AutomaticEntityForm):
    """override automatic form for ParameterValueFile entity so file input is
    shown despite optional ('?') cardinality
    """
    __select__ = autoform.AutomaticEntityForm.__select__ & is_instance('ParameterValueFile')

    def should_display_inline_creation_form(self, rschema, existant, card):
        if rschema == 'value_file':
            return not existant
        return super(ParameterValueFileEditForm, self).should_display_inline_creation_form(
            rschema, existant, card)

    def should_display_add_new_relation_link(self, rschema, existant, card):
        if rschema == 'value_file':
            return False
        return super(ParameterValueFileEditForm, self).should_display_add_new_relation_link(
            rschema, existant, card)


def pdef(form):
    """return the parameter definition object associated with a parameter value"""
    try:
        pdef_field = form.field_by_name('param_def', 'subject')
    except FieldNotFound:
        return form.edited_entity.pdef
    else:
        return form._cw.entity_from_eid(pdef_field.value)


class ParameterValueFormRenderer(formrenderers.EntityInlinedFormRenderer):
    __select__ = (formrenderers.EntityInlinedFormRenderer.__select__
                  & is_instance('ParameterValueInt',
                                'ParameterValueFloat',
                                'ParameterValueString',
                                'ParameterValueFile'))

    fieldset_css_class = table_class = u''

    def render(self, w, form, values):
        form.add_media()
        self.render_fields(w, form, values)

    def render_label(self, form, field):
        attrs = {'for': field.dom_id(form)}
        attrs['class'] = 'required'
        return tags.label(pdef(form).name, **attrs)

    def render_help(self, form, field):
        descr = pdef(form).description
        if descr:
            return u'<div class="helper">%s</div>' % descr
        return u''


class FileFormRenderer(formrenderers.EntityInlinedFormRenderer):
    __select__ = (formrenderers.EntityInlinedFormRenderer.__select__
                  & is_instance('File'))

    fieldset_css_class = table_class = u''
    display_label = False

    def render(self, w, form, values):
        form.add_media()
        self.render_fields(w, form, values)
