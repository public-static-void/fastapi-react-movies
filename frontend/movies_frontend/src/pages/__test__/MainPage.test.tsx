import { vi } from 'vitest';
import '@testing-library/jest-dom';
import MainPage from '../MainPage';
import user from '@testing-library/user-event';
import type {
  HTTPExceptionType,
  MessageType,
  MovieFileType,
  MovieType,
} from '../../types/api';
import {
  actors,
  categories,
  sawActors,
  sawMovie,
  tgf2Movie,
} from '../../mocks/defaults';
import { render, screen, waitFor } from '../../test-utils';
import type { MovieUpdateQueryType } from '../../types/state';
import { backend } from '../../mocks/handlers';
import type { PathParams } from 'msw';
import { http, HttpResponse } from 'msw';
import { server } from '../../mocks/server';

describe('Test MainPage', () => {
  const actorName = 'Danny Glover';
  const movieName = 'Saw';
  beforeEach(async () => {
    render(<MainPage />);
    await waitFor(() =>
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument()
    );
    const moviesList = await screen.findByTestId('movies-listbox');
    await user.selectOptions(moviesList, '2');
  });

  describe('Test Movie Selection', () => {
    it('Fills out the form when a movie is selected', async () => {
      const removeButton = screen.getByRole('button', { name: /remove/i });
      const updateButton = screen.getByRole('button', { name: /update/i });
      await waitFor(() => expect(updateButton).toBeEnabled());
      await waitFor(() => expect(removeButton).toBeEnabled());
      const movieNames: HTMLSelectElement[] =
        await screen.findAllByDisplayValue(movieName);
      expect(movieNames[0]).toBeEnabled();
      const studioCombobox: HTMLSelectElement =
        await screen.findByLabelText('Studio');
      await waitFor(() => {
        expect(studioCombobox).toBeEnabled();
        expect(studioCombobox.value).toBe('5');
      });
      const seriesCombobox: HTMLSelectElement =
        await screen.findByLabelText('Series');
      await waitFor(() => {
        expect(seriesCombobox).toBeEnabled();
        expect(seriesCombobox.value).toBe('2');
      });
      const categoryCheckbox: HTMLInputElement = await screen.findByRole(
        'checkbox',
        { name: 'Horror' }
      );
      await waitFor(() => {
        expect(categoryCheckbox).toBeEnabled();
        expect(categoryCheckbox).toBeChecked();
        expect(categoryCheckbox.checked).toBe(true);
      });
      const sawActorsIds = actors
        .filter((actor) => sawActors.includes(actor.name))
        .map((actor) => actor.id);
      for (const id of sawActorsIds) {
        const actorElement = await screen.findByTestId(`actors-selected-${id}`);
        expect(actorElement).toBeInTheDocument();
      }
      const seriesNumber: HTMLInputElement = screen.getByRole('textbox', {
        name: 'Series #',
      });
      expect(seriesNumber.value).toBe('1');
    });
  });

  describe('Test Actor Selection', () => {
    const getActor = (name: string) => {
      return actors.find((actor) => actor.name === name);
    };
    const addAvailableActor = async (name: string) => {
      const id = getActor(name)!.id;
      const listbox = await screen.findByRole('listbox', { name: 'Available' });
      const option = await screen.findByTestId(`actors-available-${id}`);
      await user.selectOptions(listbox, option);
      await user.dblClick(option);
    };
    const removeSelectedActor = async (name: string) => {
      const id = getActor(name)!.id;
      const listbox = await screen.findByRole('listbox', { name: 'Selected' });
      const option = await screen.findByTestId(`actors-selected-${id}`);
      await user.selectOptions(listbox, option);
      await user.dblClick(option);
    };

    it('Fails to add duplicate actor Danny Glover to movie Saw', async () => {
      const message = `Actor ${actorName} is already in ${movieName}`;
      server.use(
        http.post<PathParams, HTTPExceptionType>(
          backend('/movie_actor'),
          () => {
            return HttpResponse.json(
              {
                detail: {
                  message: message,
                },
              },
              { status: 409 }
            );
          }
        )
      );
      await addAvailableActor(actorName);
      expect(await screen.findByText(message)).toBeInTheDocument();
    });

    it('Successfully adds Al Pacino to Saw', async () => {
      const actorName = 'Al Pacino';
      const message = `Successfully added ${actorName} to ${movieName}`;
      server.use(
        http.get<PathParams, MovieType>(backend('/movies/:id'), () => {
          return HttpResponse.json({
            ...sawMovie,
            actors: [...sawMovie.actors, getActor(actorName)],
          });
        })
      );
      await addAvailableActor(actorName);
      expect(await screen.findByText(message)).toBeInTheDocument();
      expect(
        await screen.findByTestId(`actors-selected-${getActor(actorName)!.id}`)
      ).toBeInTheDocument();
    });

    it('Fails to remove Danny Glover from Saw', async () => {
      const message = `Failed to remove actor ${actorName} from ${movieName}`;
      server.use(
        http.delete<PathParams, HTTPExceptionType>(
          backend('/movie_actor'),
          () => {
            return HttpResponse.json(
              {
                detail: {
                  message: message,
                },
              },
              { status: 404 }
            );
          }
        )
      );
      await removeSelectedActor(actorName);
      expect(await screen.findByText(message)).toBeInTheDocument();
      expect(
        await screen.findByTestId(`actors-selected-${getActor(actorName)!.id}`)
      ).toBeInTheDocument();
    });

    it('Successfully removes Danny Glover from Saw', async () => {
      const message = `Successfully removed ${actorName} from ${movieName}`;
      server.use(
        http.get<PathParams, MovieType>(backend('/movies/:id'), () => {
          return HttpResponse.json({
            ...sawMovie,
            actors: sawMovie.actors.filter((actor) => actor.name !== actorName),
          });
        })
      );
      await removeSelectedActor(actorName);
      expect(await screen.findByText(message)).toBeInTheDocument();
      const actorId = getActor(actorName)!.id;
      if (actorId !== undefined) {
        await waitFor(() => {
          expect(
            screen.queryByTestId(`actors-selected-${actorId}`)
          ).not.toBeInTheDocument();
        });
      }
    });
  });

  describe('Test CategorySelector Changes', () => {
    const getCategoryCheckbox = async (name: string, checked = true) => {
      const category: HTMLInputElement = await screen.findByRole('checkbox', {
        name,
      });
      await waitFor(() => expect(category.checked).toBe(checked));
      return category;
    };

    it('Fails to remove the Horror category from Saw', async () => {
      const categoryName = 'Horror';
      const message = `Failed to remove category ${categoryName} from ${movieName}`;
      server.use(
        http.delete<PathParams, HTTPExceptionType>(
          backend('/movie_category'),
          () => {
            return HttpResponse.json(
              {
                detail: { message: message },
              },
              { status: 404 }
            );
          },
          { once: true }
        )
      );
      const checkbox = await getCategoryCheckbox(categoryName);
      await user.click(checkbox);
      expect(await screen.findByText(message)).toBeInTheDocument();
      await waitFor(() => expect(checkbox.checked).toBe(true));
    });

    it('Successfully removes Horror category from Saw', async () => {
      const categoryName = 'Horror';
      const message = `Successfully removed category ${categoryName} from ${movieName}`;
      server.use(
        http.get<PathParams, MovieType>(backend('/movies/:id'), () => {
          return HttpResponse.json({
            ...sawMovie,
            categories: [],
          });
        })
      );
      const checkbox = await getCategoryCheckbox(categoryName);
      await user.click(checkbox);
      expect(await screen.findByText(message)).toBeInTheDocument();
      await waitFor(() => expect(checkbox.checked).toBe(false));
    });

    it('Fails to add Action category to Saw', async () => {
      const categoryName = 'Action';
      const message = `Failed to add category ${categoryName} to ${movieName}`;
      server.use(
        http.post<PathParams, HTTPExceptionType>(
          backend('/movie_category'),
          () => {
            return HttpResponse.json(
              {
                detail: { message: message },
              },
              { status: 404 }
            );
          },
          { once: true }
        )
      );
      const checkbox = await getCategoryCheckbox(categoryName, false);
      await user.click(checkbox);
      expect(await screen.findByText(message)).toBeInTheDocument();
      await waitFor(() => expect(checkbox.checked).toBe(false));
    });

    it('Successfully adds Action category to Saw', async () => {
      const categoryName = 'Action';
      const message = `Successfully added category ${categoryName} to ${movieName}`;
      server.use(
        http.get<PathParams, MovieType>(backend('/movies/:id'), () => {
          return HttpResponse.json({
            ...sawMovie,
            categories: [
              ...sawMovie.categories,
              categories.find((category) => category.name === categoryName),
            ],
          });
        })
      );
      const checkbox = await getCategoryCheckbox(categoryName, false);
      await user.click(checkbox);
      expect(await screen.findByText(message)).toBeInTheDocument();
      await waitFor(() => expect(checkbox.checked).toBe(true));
    });
  });
});

describe('Test MovieDataForm', () => {
  let nameField: HTMLInputElement;
  let studioSelector: HTMLSelectElement;
  let seriesSelector: HTMLSelectElement;
  let seriesNumberField: HTMLInputElement;
  let updateButton: HTMLButtonElement;
  let removeButton: HTMLButtonElement;

  beforeEach(async () => {
    render(<MainPage />);
    await waitFor(() =>
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument()
    );
    await screen.findByTestId('movies-listbox');
    nameField = screen.getByRole('textbox', { name: 'Name' });
    studioSelector = screen.getByRole('combobox', { name: 'Studio' });
    seriesSelector = screen.getByRole('combobox', { name: 'Series' });
    seriesNumberField = screen.getByRole('textbox', { name: 'Series #' });
    updateButton = screen.getByRole('button', { name: /update/i });
    removeButton = screen.getByRole('button', { name: /remove/i });
  });

  it('Successfully changes Saw -> The Godfather Part II', async () => {
    server.use(
      http.put<PathParams, MovieUpdateQueryType, MovieType>(
        backend('/movies/:id'),
        () => {
          return HttpResponse.json(tgf2Movie);
        }
      )
    );
    server.use(
      http.get<PathParams, MovieType>(backend('/movies/:id'), () => {
        return HttpResponse.json(tgf2Movie);
      })
    );
    server.use(
      http.get<PathParams, MovieFileType[]>(backend('/movies'), () => {
        return HttpResponse.json([{ id: 1, filename: tgf2Movie.filename }]);
      })
    );
    await waitFor(async () => {
      await user.clear(nameField);
      expect(nameField).toHaveValue('');
    });
    await user.type(nameField, tgf2Movie.name!);
    expect(nameField.value).toBe(tgf2Movie.name);
    const studioId = tgf2Movie.studio!.id.toString();
    await user.selectOptions(studioSelector, studioId);
    expect(studioSelector.value).toBe(studioId);
    const seriesId = tgf2Movie.series?.id.toString() ?? '';
    await user.selectOptions(seriesSelector, seriesId);
    expect(seriesSelector.value).toBe(seriesId);
    const seriesNumber = tgf2Movie.series_number!.toString();
    await waitFor(async () => {
      await user.clear(seriesNumberField);
      expect(seriesNumberField).toHaveValue('');
    });
    await user.type(seriesNumberField, seriesNumber);
    expect(seriesNumberField.value).toBe(seriesNumber);
    await user.click(updateButton);
    const statusText = await screen.findByText(
      'Successfully updated movie The Godfather Part II'
    );
    expect(statusText).toBeInTheDocument();
    await screen.findByRole('option', { name: tgf2Movie.filename });
  });

  it('Successfully removes Godfather Part II', async () => {
    server.use(
      http.get<PathParams, MovieFileType[]>(backend('/movies'), () => {
        return HttpResponse.json([]);
      })
    );
    server.use(
      http.delete<PathParams, MessageType>(backend('/movies/:id'), () => {
        return HttpResponse.json({
          message: `Successfully removed movie ${tgf2Movie.name}`,
        });
      })
    );
    const movieListOption = await screen.findByRole('option', {
      name: tgf2Movie.filename,
    });
    const confirmSpy = vi.spyOn(window, 'confirm');
    confirmSpy.mockImplementation(vi.fn(() => true));
    await user.click(removeButton);
    expect(window.confirm).toHaveBeenCalled();
    confirmSpy.mockRestore();
    await waitFor(() => {
      expect(movieListOption).not.toBeInTheDocument();
    });
    await waitFor(() => {
      expect(nameField.value).toBe('');
      expect(nameField).toBeDisabled();
    });
    await waitFor(() => {
      expect(studioSelector.value).toBe('');
      expect(studioSelector).toBeDisabled();
    });
    await waitFor(() => {
      expect(seriesSelector.value).toBe('');
      expect(seriesSelector).toBeDisabled();
    });
    await waitFor(() => {
      expect(seriesNumberField.value).toBe('');
      expect(seriesNumberField).toBeDisabled();
    });
    await waitFor(() => {
      expect(removeButton).toBeDisabled();
      expect(updateButton).toBeDisabled();
    });
    const checkboxes: HTMLInputElement[] =
      await screen.findAllByRole('checkbox');
    for (const checkbox of checkboxes) {
      await waitFor(() => {
        expect(checkbox.checked).toBe(false);
        expect(checkbox).toBeDisabled();
      });
    }
    await waitFor(() => {
      expect(screen.getByRole('listbox', { name: 'Available' })).toBeDisabled();
    });
    await screen.findByRole('heading', { name: 'None' });
    expect(screen.queryByRole('listbox', { name: 'Selected' })).toBeNull();
  });
});
