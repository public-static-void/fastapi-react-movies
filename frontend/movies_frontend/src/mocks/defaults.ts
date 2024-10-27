import {
  ActorType,
  CategoryType,
  MovieFileType,
  MovieType,
  SeriesType,
  StudioType,
} from '../types/api';

export const actors: ActorType[] = [
  { id: 1, name: 'Al Pacino' },
  { id: 2, name: 'Robert De Niro' },
  { id: 3, name: 'Marlon Brando' },
  { id: 4, name: 'Christian Bale' },
  { id: 5, name: 'Danny Glover' },
];

export const categories: CategoryType[] = [
  { id: 1, name: 'Horror' },
  { id: 2, name: 'Crime' },
  { id: 3, name: 'Action' },
  { id: 4, name: 'Drama' },
  { id: 5, name: 'Comedy' },
];

export const movies: MovieFileType[] = [
  { id: 1, filename: 'The Godfather' },
  { id: 2, filename: '[Twisted] {Saw 1} Saw (Danny Glover).mp4' },
  { id: 3, filename: 'The Matrix' },
  { id: 4, filename: 'Star Wars' },
  { id: 5, filename: 'Lord of the Rings' },
];

export const series: SeriesType[] = [
  { id: 1, name: 'The Godfather' },
  { id: 2, name: 'Saw' },
  { id: 3, name: 'The Matrix' },
  { id: 4, name: 'Star Wars' },
  { id: 5, name: 'Lord of the Rings' },
];

export const studios: StudioType[] = [
  { id: 1, name: 'Warner Bros' },
  { id: 2, name: 'Universal' },
  { id: 3, name: 'Paramount' },
  { id: 4, name: '20th Century Fox' },
  { id: 5, name: 'Twisted' },
];

export const sawActors = ['Danny Glover'];

export const sawMovie: MovieType = {
  id: movies[1]?.id ?? 2,
  filename: movies[1]?.filename ?? '[Twisted] {Saw 1} Saw (Danny Glover).mp4',
  name: 'Saw',
  actors: actors.filter((actor) => sawActors.includes(actor.name)),
  categories: categories.filter((category) => category.name === 'Horror'),
  series: series.find((series) => series?.name === 'Saw') ?? null,
  series_number: 1,
  studio: studios.find((studio) => studio?.name === 'Twisted') ?? null,
};

export const tgf2Actors = ['Al Pacino', 'Robert De Niro'];

export const tgf2Movie: MovieType = {
  id: movies[5]?.id ?? 6,
  filename:
    movies[5]?.filename ??
    '[Paramount] {The Godfather} The Godfather Part II (Al Pacino, Robert De Niro).mp4',
  name: 'The Godfather Part II',
  actors: actors.filter((actor) => tgf2Actors.includes(actor.name)),
  categories: categories.filter((category) => category.name === 'Crime'),
  series: series.find((series) => series?.name === 'The Godfather') ?? null,
  series_number: 2,
  studio: studios.find((studio) => studio?.name === 'Paramount') ?? null,
};
