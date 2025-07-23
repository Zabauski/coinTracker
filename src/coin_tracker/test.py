import matplotlib.pyplot as plt
from textual.app import App
from textual.widgets import Static
from io import BytesIO
from PIL import Image

class PieChartApp(App):
    async def on_mount(self):
        # Данные для круговой диаграммы
        labels = ['Категория A', 'Категория B', 'Категория C']
        sizes = [30, 45, 25]

        # Создание круговой диаграммы с помощью matplotlib
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Круговая диаграмма выглядит как круг

        # Сохранение диаграммы в буфер
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Загрузка изображения с помощью PIL
        image = Image.open(buf)

        # Отображение изображения в виджете Textual
        widget = Static()
        widget.update(image)
        await self.view.dock(widget)

if __name__ == "__main__":
    PieChartApp.run()

