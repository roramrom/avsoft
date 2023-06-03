import socket
import time
import matplotlib.pyplot as plt
import matplotlib
from urllib.parse import urlparse

# Использование режима "Agg" для Matplotlib, чтобы не требовался графический интерфейс
matplotlib.use("Agg")

class WebsiteScanner:
    def __init__(self, website_url):
        self.website_url = website_url
        self.parsed_url = urlparse(website_url)
        self.host = self.parsed_url.netloc.split(":")[0]  # Получаем хост из URL
        self.port = 80  # Порт для HTTP-запроса
        self.request = f"GET {website_url} HTTP/1.1\r\nHost: {self.host}\r\n\r\n"  # Запрос для отправки

    def send_http_request(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.host, self.port))
            s.sendall(self.request.encode())

            response = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                response += data

            return response.decode()

        finally:
            s.close()

    def count_urls(self, response):
        urls = response.split("http://")
        num_urls = len(urls) - 1
        return num_urls

    def process_website(self):
        start_time = time.time()
        response = self.send_http_request()
        end_time = time.time()
        elapsed_time = end_time - start_time
        num_urls = self.count_urls(response)
        return [self.website_url, "{:.2f}".format(elapsed_time), str(num_urls), self.parsed_url.netloc], response

    def get_domain_name(self):
        return self.parsed_url.netloc.split(":")[0]


def main():
    website_urls = input("Введите URL-адреса веб-сайтов (через запятую): ").split(",")
    website_urls = [url.strip() for url in website_urls]

    table_data = [["URL сайта", "Время обработки (сек)", "Кол-во найденных ссылок", "Имя файла с результатом"]]

    with open("site.txt", "w") as file:
        for website_url in website_urls:
            website = WebsiteScanner(website_url)
            result, response = website.process_website()
            table_data.append(result)

            file.write("URL сайта: {}\n".format(result[0]))
            file.write("Время обработки (сек): {}\n".format(result[1]))
            file.write("Кол-во найденных ссылок: {}\n".format(result[2]))
            file.write("Имя файла с результатом: {}\n".format(result[3]))
            file.write("\n")
            file.write(response)
            file.write("\n\n")

    with open("result.txt", "w") as log_file:
        log_file.write("Файл с результатами: site.txt\n\n")
        for result in table_data[1:]:
            log_file.write("URL сайта: {}\n".format(result[0]))
            log_file.write("Время обработки (сек): {}\n".format(result[1]))
            log_file.write("Кол-во найденных ссылок: {}\n".format(result[2]))
            log_file.write("Имя файла с результатом: site.txt\n")
            log_file.write("\n")

    num_rows = len(table_data)
    num_cols = len(table_data[0])

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis("off")

    table = ax.table(cellText=table_data,
                     loc="center",
                     colLabels=None,
                     cellLoc="center",
                     colWidths=[0.25, 0.25, 0.25, 0.25])

    table.auto_set_font_size(False)
    table.set_fontsize(12)

    max_word_length = max(len(word) for row in table_data for word in row)
    table.scale(1, 1.5 * num_rows / num_cols * max_word_length / 10)

    plt.savefig("site.png")
    plt.close()

    print("Результаты сохранены:")
    print("Таблица сохранена в: site.png")
    print("Файл результатов: site.txt")

if __name__ == "__main__":
    main()
