import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import type {
  ActorType,
  CategoryType,
  MovieFileType,
  MovieType,
  SeriesType,
  StudioType,
} from '../types/api';
import type {
  MovieActorAssociationtype,
  MovieCategoryAssociationtype,
  MoviePropertyType,
  MovieUpdateQueryType,
} from '../types/state';

let baseUrl: string;
if (typeof import.meta.env.VITE_BACKEND !== 'string') {
  baseUrl = 'http://localhost:8000';
} else {
  baseUrl = import.meta.env.VITE_BACKEND;
}

export const MovieManagerApi = createApi({
  reducerPath: 'movieManagerApi',
  tagTypes: ['movies', 'movie', 'actors', 'categories', 'series', 'studios'],
  baseQuery: fetchBaseQuery({
    baseUrl: baseUrl,
  }),
  endpoints: (builder) => ({
    actorAdd: builder.mutation<ActorType, MoviePropertyType>({
      query: ({ ...body }) => ({
        url: '/actors',
        method: 'POST',
        body: body,
      }),
      invalidatesTags: ['actors'],
    }),
    actorDelete: builder.mutation<void, MoviePropertyType>({
      query: ({ id }) => ({ url: `/actors/${id}`, method: 'DELETE' }),
      invalidatesTags: ['actors'],
    }),
    actorUpdate: builder.mutation<ActorType, MoviePropertyType>({
      query: ({ id, ...body }) => ({
        url: `/actors/${id}`,
        method: 'PUT',
        body: body,
      }),
      invalidatesTags: ['actors', 'movie', 'movies'],
    }),
    actors: builder.query<ActorType[], void>({
      query: () => '/actors',
      providesTags: ['actors'],
    }),
    categories: builder.query<CategoryType[], void>({
      query: () => '/categories',
      providesTags: ['categories'],
    }),
    categoryAdd: builder.mutation<CategoryType, MoviePropertyType>({
      query: ({ ...body }) => ({
        url: '/categories',
        method: 'POST',
        body: body,
      }),
      invalidatesTags: ['categories'],
    }),
    categoryDelete: builder.mutation<void, MoviePropertyType>({
      query: ({ id }) => ({ url: `/categories/${id}`, method: 'DELETE' }),
      invalidatesTags: ['categories'],
    }),
    categoryUpdate: builder.mutation<CategoryType, MoviePropertyType>({
      query: ({ id, ...body }) => ({
        url: `/categories/${id}`,
        method: 'PUT',
        body: body,
      }),
      invalidatesTags: ['categories', 'movie'],
    }),
    movie: builder.query<MovieType, string>({
      query: (id) => `/movies/${id}`,
      providesTags: ['movie'],
    }),
    movieActorAdd: builder.mutation<MovieType, MovieActorAssociationtype>({
      query: ({ actorId, movieId }) => ({
        url: `/movie_actor?movie_id=${movieId}&actor_id=${actorId}`,
        method: 'POST',
      }),
      invalidatesTags: ['movie', 'movies'],
    }),
    movieActorDelete: builder.mutation<MovieType, MovieActorAssociationtype>({
      query: ({ actorId, movieId }) => ({
        url: `/movie_actor?movie_id=${movieId}&actor_id=${actorId}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['movie', 'movies'],
    }),
    movieCategoryAdd: builder.mutation<MovieType, MovieCategoryAssociationtype>(
      {
        query: ({ categoryId, movieId }) => ({
          url: `/movie_category?movie_id=${movieId}&category_id=${categoryId}`,
          method: 'POST',
        }),
        invalidatesTags: ['movie'],
      }
    ),
    movieCategoryDelete: builder.mutation<
      MovieType,
      MovieCategoryAssociationtype
    >({
      query: ({ categoryId, movieId }) => ({
        url: `/movie_category?movie_id=${movieId}&category_id=${categoryId}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['movie'],
    }),
    movieDelete: builder.mutation<void, string>({
      query: (id) => ({ url: `/movies/${id}`, method: 'DELETE' }),
      invalidatesTags: ['movies'],
    }),
    movieUpdate: builder.mutation<MovieType, MovieUpdateQueryType>({
      query: ({ id, ...body }) => ({
        url: `/movies/${id}`,
        method: 'PUT',
        body: body,
      }),
      invalidatesTags: ['movie', 'movies'],
    }),
    movies: builder.query<MovieFileType[], void>({
      query: () => '/movies',
      providesTags: ['movies'],
    }),
    moviesImport: builder.mutation<MovieFileType[], void>({
      query: () => ({ url: '/movies', method: 'POST' }),
      invalidatesTags: ['movies'],
    }),
    series: builder.query<SeriesType[], void>({
      query: () => '/series',
      providesTags: ['series'],
    }),
    seriesAdd: builder.mutation<SeriesType, MoviePropertyType>({
      query: ({ ...body }) => ({
        url: '/series',
        method: 'POST',
        body: body,
      }),
      invalidatesTags: ['series'],
    }),
    seriesDelete: builder.mutation<void, MoviePropertyType>({
      query: ({ id }) => ({ url: `/series/${id}`, method: 'DELETE' }),
      invalidatesTags: ['series'],
    }),
    seriesUpdate: builder.mutation<SeriesType, MoviePropertyType>({
      query: ({ id, ...body }) => ({
        url: `/series/${id}`,
        method: 'PUT',
        body: body,
      }),
      invalidatesTags: ['series', 'movie', 'movies'],
    }),
    studioAdd: builder.mutation<StudioType, MoviePropertyType>({
      query: ({ ...body }) => ({
        url: '/studios',
        method: 'POST',
        body: body,
      }),
      invalidatesTags: ['studios'],
    }),
    studioDelete: builder.mutation<void, MoviePropertyType>({
      query: ({ id }) => ({ url: `/studios/${id}`, method: 'DELETE' }),
      invalidatesTags: ['studios'],
    }),
    studioUpdate: builder.mutation<StudioType, MoviePropertyType>({
      query: ({ id, ...body }) => ({
        url: `/studios/${id}`,
        method: 'PUT',
        body: body,
      }),
      invalidatesTags: ['studios', 'movie', 'movies'],
    }),
    studios: builder.query<StudioType[], void>({
      query: () => '/studios',
      providesTags: ['studios'],
    }),
  }),
});

export const {
  useActorAddMutation,
  useActorDeleteMutation,
  useActorUpdateMutation,
  useActorsQuery,
  useCategoriesQuery,
  useCategoryAddMutation,
  useCategoryDeleteMutation,
  useCategoryUpdateMutation,
  useMovieActorAddMutation,
  useMovieActorDeleteMutation,
  useMovieCategoryAddMutation,
  useMovieCategoryDeleteMutation,
  useMovieDeleteMutation,
  useMovieQuery,
  useMovieUpdateMutation,
  useMoviesImportMutation,
  useMoviesQuery,
  useSeriesAddMutation,
  useSeriesDeleteMutation,
  useSeriesQuery,
  useSeriesUpdateMutation,
  useStudioAddMutation,
  useStudioDeleteMutation,
  useStudioUpdateMutation,
  useStudiosQuery,
} = MovieManagerApi;
