from colorful.widgets import ColorFieldWidget
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import format_html

__author__ = 'M.Y'


class ColorHexFieldWidget(ColorFieldWidget):
    input_type = 'text'
    # def render(self, name, value, attrs={}):
    #     content = super(ColorHexFieldWidget, self).render(name, value, attrs)
    #
    #     if value is None:
    #         value = ''
    #     final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
    #     if value != '':
    #         # Only add the 'value' attribute if a value is non-empty.
    #         final_attrs['value'] = force_text(self._format_value(value))
    #
    #     final_attrs['id'] += 'hex'
    #     final_attrs['name'] += 'hex'
    #     final_attrs['type'] = 'text'
    #     final_attrs['style'] = "width: 60px !important;margin: 2px;direction: ltr;"
    #
    #     content += format_html('<input{} />', flatatt(final_attrs))
    #
    #     content += '''<script type="text/javascript">
    #                 (function($){
    #                     $(document).ready(function(){
    #                         $("#%(id)s").bind("change paste keyup", function() {
    #                             var val = $(this).val();
    #                             $("#%(hexid)s").val(val);
    #                         });
    #                         $("#%(hexid)s").bind("change paste keyup", function() {
    #                             var val = $(this).val();
    #                             if(val.length == 7)
    #                                 $("#%(id)s").val(val);
    #                         });
    #                     });
    #                 })('django' in window && django.jQuery ? django.jQuery: jQuery);
    #             </script>
    #             ''' % {'id': attrs['id'], 'hexid': final_attrs['id']}
    #
    #     return content
