from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.forms.widgets import flatatt
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from pagedown.widgets import AdminPagedownWidget as OriginalAPW

from django.contrib.staticfiles.storage import staticfiles_storage as static


class AdminPagedownWidget(OriginalAPW):
    class Media:
        css = {'all': (static.url('css/overcast/jquery-ui-1.8.20.custom.css'),
                       static.url('ladmin/limage-customizations.css'),
                       static.url('ladmin/lstory-customizations.css'),
                       static.url('text.css'),)}
        js = (static.url('js/jquery-1.7.2.min.js'),
              static.url('js/jquery-ui-1.8.20.custom.min.js'),
              static.url('js/jquery.form.js'),
              static.url('js/admin/jquery.textarea.js'),
              static.url('js/admin/powerhour.messageboxes.js'),
              static.url('limage-pagedown.js'),
              static.url('js/jquery-fullscreen-textarea.js'),
              static.url('text.js'),)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        if 'class' not in attrs:
            attrs['class'] = ""
        attrs['class'] += " wmd-input"
        final_attrs = self.build_attrs(attrs, name=name)
        html = """
            <div class="wmd-wrapper">
                <div class="wmd-panel">
                <div id="%(id)s_wmd_button_bar"></div>
                <textarea%(attrs)s>%(body)s</textarea>
                </div>
                <div id="%(id)s_wmd_preview" class="wmd-panel wmd-preview"></div>
                <div id="%(id)s_wmd_dialog"></div>
            </div>
            <script type="text/javascript">
                var editors = editors?editors:[];
                (function () {
                    var converter = Markdown.getSanitizingConverter();
                    selectors = {
                        input : "%(id)s",
                        button : "%(id)s_wmd_button_bar",
                        preview : "%(id)s_wmd_preview",
                    }
                    var help = function(x) {
                        alert('ohai');
                    };
                    var editor = new Markdown.Editor(converter, selectors);
                    editor.run();
                    editors.push(editor);

                    lImage_pagedown.extend("./images/", "%(id)s_wmd_dialog", editor);
                    lStory_pagedown.extend(editor);
                    $('#'+selectors.input).fullTextArea();
                })();
            </script>
            """ % {'attrs': flatatt(final_attrs),
                   'body': conditional_escape(force_unicode(value)),
                   'id': attrs['id'], }
        return mark_safe(html)
