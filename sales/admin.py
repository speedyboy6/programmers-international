from django.contrib import admin
from .models import Category, Product, Enquiry
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from io import BytesIO

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'email', 'phone_number', 'enquired_at', 'status')
    list_filter = ('status', 'enquired_at') # Added 'enquired_at' for date filtering
    search_fields = ('name', 'email', 'product__name')
    actions = ['export_as_pdf'] # Enable PDF export action

    def export_as_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="enquiries_report.pdf"'

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Start writing the PDF here
        p.setFont("Helvetica-Bold", 16)
        p.drawString(inch, height - inch, "Enquiries Report")

        p.setFont("Helvetica", 9) # Smaller font for table data
        textobject = p.beginText(inch, height - 1.5 * inch)
        # Header - adjust spacing/columns as needed
        header = f"{'Product':<25} | {'Enquirer':<20} | {'Email':<25} | {'Phone':<15} | {'Qty':<5} | {'Enquired At':<20} | {'Status':<10}"
        textobject.textLine(header)
        textobject.textLine("-" * 130) # Separator line
        textobject.moveCursor(0, 12) # Move down for next line

        line_height = 12
        y_position = height - 1.5 * inch - line_height * 2 # Initial Y position for data

        for enquiry in queryset:
            # Check if we need a new page
            if y_position < inch:
                p.drawText(textobject)
                p.showPage()
                p.setFont("Helvetica", 9)
                textobject = p.beginText(inch, height - 1.5 * inch)
                textobject.textLine(header) # Redraw header on new page
                textobject.textLine("-" * 130)
                textobject.moveCursor(0, 12)
                y_position = height - 1.5 * inch - line_height * 2

            line = f"{enquiry.product.name[:23]:<25} | {enquiry.name[:18]:<20} | {enquiry.email[:23]:<25} | {enquiry.phone_number[:13]:<15} | {str(enquiry.quantity):<5} | {enquiry.enquired_at.strftime('%Y-%m-%d %H:%M'):<20} | {enquiry.status:<10}"
            textobject.textLine(line)
            y_position -= line_height

        p.drawText(textobject)
        p.showPage()
        p.save()

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    export_as_pdf.short_description = "Export selected enquiries as PDF"
