from urllib.request import urlopen
from bs4 import BeautifulSoup


def distributor(soup):
    distributors = soup.find_all('td', class_='a-text-left mojo-field-type-release_studios')
    distributor_dict = {}

    for i in range(len(distributors)):
        distributors_text = distributors[i].get_text(strip=True)
        distributor_dict[distributors_text] = distributor_dict.get(distributors_text, 0) + 1

    maximum = 0
    max_distributor = ''
    for dist, number in distributor_dict.items():
        if number > maximum:
            maximum = number
            max_distributor = dist

    return max_distributor, maximum


def weeks_released(weeks_released_list, titles):
    weeks_list = []

    for i in range(len(weeks_released_list)):
        weeks_released_text = int(weeks_released_list[i].get_text(strip=True))
        weeks_list.append(weeks_released_text)

    most_weeks = max(weeks_list)
    index_of_most_weeks = weeks_list.index(most_weeks)

    return titles[index_of_most_weeks].get_text(), most_weeks


def movie_rank_change(rank_changes, titles):
    # Filter out None values temporarily to check max and min
    valid_rank_changes = [i for i in rank_changes if i is not None]
    biggest_gain_value = max(valid_rank_changes)
    biggest_loss_value = min(valid_rank_changes)
    biggest_gains = []
    biggest_losses = []

    for i, change in enumerate(rank_changes):
        if change == biggest_gain_value:
            biggest_gains.append(titles[i].get_text(strip=True))
        elif change == biggest_loss_value:
            biggest_losses.append(titles[i].get_text(strip=True))

    return biggest_gains, biggest_gain_value, biggest_losses, biggest_loss_value


def main():
    url = 'http://boxofficemojo.com/weekend/chart/'
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    date_element = soup.find('h4', class_='mojo-gutter')
    titles = soup.find_all('td', class_='a-text-left mojo-field-type-release mojo-cell-wide')
    last_week_ranks_and_weeks_in = soup.find_all('td', class_='a-text-right mojo-field-type-positive_integer')
    all_grosses = soup.find_all('td', class_='a-text-right mojo-field-type-money mojo-estimatable')
    ranks = soup.find_all('td', class_='a-text-right mojo-header-column mojo-truncate mojo-field-type-rank '
                                       'mojo-sort-column')

    # week and total elements have the same class and parents so I went about separating them in an odd way
    week_gross = [all_grosses[i] for i in range(0, len(all_grosses), 3)]
    total_gross = [all_grosses[i] for i in range(2, len(all_grosses), 3)]
    # the last list was finding more instances of the same class so I skipped over the other instance as seen below
    last_week_ranks = [last_week_ranks_and_weeks_in[i] for i in range(0, len(last_week_ranks_and_weeks_in), 2)]
    weeks_released_list = [last_week_ranks_and_weeks_in[i] for i in range(1, len(last_week_ranks_and_weeks_in), 2)]

    most_weeks_movie_title, most_weeks_number = weeks_released(weeks_released_list, titles)

    debuts = soup.find_all('tr', class_='mojo-annotation-isNewThisWeek')
    number_debuts = len(debuts)
    strongest_debut_title = debuts[0].find('td', class_='a-text-left mojo-field-type-release mojo-cell-wide').get_text(
        strip=True)
    weakest_debut_title = debuts[-1].find('td', class_='a-text-left mojo-field-type-release mojo-cell-wide').get_text(
        strip=True)

    strongest_debut_rank = debuts[0].find('td', class_='a-text-right mojo-header-column mojo-truncate '
                                                       'mojo-field-type-rank mojo-sort-column').get_text(
        strip=True)

    weakest_debut_rank = debuts[-1].find('td', class_='a-text-right mojo-header-column mojo-truncate '
                                                      'mojo-field-type-rank mojo-sort-column').get_text(
        strip=True)

    # Calculate rank changes and determine the biggest gain and loss
    rank_changes = []
    # iterate through ranks, acquire current and last weeks value and then subtract them and append to a new list
    for i in range(len(ranks)):
        current_rank_value = int(ranks[i].get_text(strip=True))
        if last_week_ranks[i].get_text(strip=True) != '-':
            last_week_rank_value = int(last_week_ranks[i].get_text(strip=True))
        else:
            last_week_rank_value = None

        if last_week_rank_value is None:
            rank_changes.append(None)
        else:
            rank_changes.append(last_week_rank_value - current_rank_value)
    print(rank_changes)

    biggest_gains, biggest_gain_value, biggest_losses, biggest_loss_value = movie_rank_change(rank_changes,
                                                                                              titles)

    # Find which distributor distributed the most
    max_distributor_name, max_number_distributed = distributor(soup)

    print(f'Movie information for the weekend of {date_element.get_text(strip=True)}:\n')
    for index, (title, last_week_rank, week, total) in enumerate(zip(titles, last_week_ranks, week_gross, total_gross),
                                                                 start=1):
        movie_title = title.get_text(strip=True)
        truncated_title = movie_title[:35]
        rank_text = last_week_rank.get_text(strip=True)
        rank_text = rank_text if rank_text else '-'  # If there is no rank, display '-'
        week_gross_text = week.get_text(strip=True)
        total_gross_text = total.get_text(strip=True)
        print(f'{index:>2} {rank_text:<2} {truncated_title:<35} {week_gross_text:<12} {total_gross_text:<12}')

    print(f'\nThere were {number_debuts} debuts this week!')
    print(f'Biggest debut was {strongest_debut_title}: ({strongest_debut_rank})')
    print(f'Weakest debut was {weakest_debut_title}: ({weakest_debut_rank})')
    print(f'Biggest gain this week was places, movies: {", ".join(biggest_gains)} ({biggest_gain_value} places)')
    print(f'Biggest loss this week was places, movies: {", ".join(biggest_losses)} ({biggest_loss_value} places)')
    print(f'Most weeks released was {most_weeks_movie_title} ({most_weeks_number} weeks)')
    print(f'Distributor with the most movies was {max_distributor_name} ({max_number_distributed} movies)')


if __name__ == '__main__':
    main()
