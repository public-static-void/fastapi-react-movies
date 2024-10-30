import { http, HttpResponse, PathParams } from 'msw';
import {
  actors,
  categories,
  sawMovie,
  movies,
  series,
  studios,
} from './defaults';
import {
  ActorType,
  CategoryType,
  HTTPExceptionType,
  MovieFileType,
  MovieType,
  SeriesType,
  StudioType,
} from '../types/api';

let baseUrl: string;
if (typeof import.meta.env.VITE_BACKEND !== 'string') {
  baseUrl = 'http://localhost:8000';
} else {
  baseUrl = import.meta.env.VITE_BACKEND;
}

export const backend = (path: string) => new URL(path, baseUrl).toString();

export const handlers = [
  http.get<PathParams, CategoryType[]>(backend('/categories'), () => {
    return HttpResponse.json(categories);
  }),
  http.get<PathParams, ActorType[]>(backend('/actors'), () => {
    return HttpResponse.json(actors);
  }),
  http.get<PathParams, SeriesType[]>(backend('/series'), () => {
    return HttpResponse.json(series);
  }),
  http.get<PathParams, StudioType[]>(backend('/studios'), () => {
    return HttpResponse.json(studios);
  }),
  http.get<PathParams, MovieFileType[]>(backend('/movies'), () => {
    return HttpResponse.json(movies);
  }),
  http.get<PathParams, MovieType>(backend('/movies/2'), () => {
    return HttpResponse.json(sawMovie);
  }),
  http.delete<PathParams, MovieType>(backend('/movie_actor'), () => {
    return HttpResponse.json({
      ...sawMovie,
      actors: sawMovie.actors.filter((actor) => actor.name !== 'Danny Glover'),
    });
  }),
  http.post<PathParams, MovieType>(backend('/movie_actor'), () => {
    return HttpResponse.json({
      ...sawMovie,
      actors: [...sawMovie.actors, actors[1]],
    });
  }),
  http.delete<PathParams, MovieType>(backend('/movie_category'), () => {
    return HttpResponse.json({
      ...sawMovie,
      categories: [],
    });
  }),
  http.post<PathParams, MovieType>(backend('/movie_category'), () => {
    return HttpResponse.json({
      ...sawMovie,
      categories: [...sawMovie.categories, categories[1]],
    });
  }),
];
