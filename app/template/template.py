from vkbottle import TemplateElement, template_gen, Keyboard
from vkbottle.tools import OpenLink

el1 = TemplateElement(
    title="1",
    description="Консультация",
    buttons=Keyboard(inline=True).add(
        OpenLink("https://example.com/1", "Купить")
    )
)

el2 = TemplateElement(
    title="2",
    description="ПУПУПУ",
    buttons=Keyboard(inline=True).add(
        OpenLink("https://example.com/1", "Купить")
    )
)

my_temp = template_gen(el1, el2)
