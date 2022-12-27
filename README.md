# Базовый CBS и улучшения

## Описание

Поиск на основе конфликтов (CBS) - это очень эффективный оптимальный алгоритм MAPF. CBS имеет два уровня. Низкоуровневый находит оптимальные пути для отдельных агентов. Если пути включают конфликты, высокий уровень посредством разделенного действия накладывает ограничения на конфликтующих агентов, чтобы избежать этих конфликтов. В этой репе мы реализуем CBS и ее улучшения CBSH, CBS Disjoint Splitting, CBS Prioritizing Conflicts

![descriptionGIF](https://user-images.githubusercontent.com/64801664/209649469-fd57a31d-2e68-4232-91a4-8d335fc1be2d.gif)



## Инструкция

Можно протестировать один из них через файл main. Флаг --file_name нужен для выбора файла с картой и --solver (default CBS, CBSH, CBS_CP, CBS_DS) для выбора алгоритма

В --file_name мы прописываем txt файл, в формате 
```
height width
map
count_of_agent
agent_1_start_point_i agent_1_start_point_j agent_1_goal_point_i agent_1_goal_point_j
...
```

Пример
```
4 7
@ @ @ @ @ @ @
@ . . . . . @
@ @ @ . @ @ @
@ @ @ @ @ @ @
2
1 1 1 5
1 2 1 4
```



## Примеры
![exampl1GIF](https://user-images.githubusercontent.com/64801664/209651497-2a384794-68d3-4890-ad7e-23846e97f20e.gif)

### Источники

[CBS](https://www.bgu.ac.il/~felner/2015/CBSjur.pdf)

[CBSH](https://www2.cs.sfu.ca/~hangma/pub/ijcai19.pdf)

[CBS_CP](https://www.ijcai.org/Proceedings/15/Papers/110.pdf)

[CBS_DS](https://people.eng.unimelb.edu.au/pstuckey/papers/icaps19a.pdf)


**Работали над проектом: Петров Леонид, Ибрагимов Артем и Никитин Максим**


