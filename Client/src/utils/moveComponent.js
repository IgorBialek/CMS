export default function moveComponent(index, direction, tab, callback) {
    if (direction == "up" && index > 0) {
      [tab[index], tab[index - 1]] = [tab[index - 1], tab[index]];
    }

    if (direction == "down" && index < tab.length - 1) {
      [tab[index], tab[index + 1]] = [tab[index + 1], tab[index]];
    }

    callback(tab);
  };