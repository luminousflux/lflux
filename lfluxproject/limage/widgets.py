from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.forms.widgets import flatatt
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from pagedown.widgets import AdminPagedownWidget as OriginalAPW


class AdminPagedownWidget(OriginalAPW):
    class Media:
        css = {'all': ('%s/css/overcast/jquery-ui-1.8.20.custom.css' % settings.STATIC_URL,
                       '%s/limage-customizations.css' % settings.STATIC_URL,)}
        js = ('%s/js/jquery-1.7.2.min.js' % settings.STATIC_URL,
              '%s/js/jquery-ui-1.8.20.custom.min.js' % settings.STATIC_URL,
              '%s/js/jquery.form.js' % settings.STATIC_URL,
              '%s/limage-pagedown.js' % settings.STATIC_URL,)

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
                    var editor = new Markdown.Editor(converter, selectors);
                    editor.run();
                    editors.push(editor);

                    lImage_pagedown.extend("./images/", "%(id)s_wmd_dialog", editor);
                })();
            </script>
            """ % {'attrs': flatatt(final_attrs),
                   'body': conditional_escape(force_unicode(value)),
                   'id': attrs['id'], }
        return mark_safe(html)
