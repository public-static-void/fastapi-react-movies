import '@testing-library/jest-dom';
import { render, screen } from '../../test-utils';
import MovieDataForm from '../MovieDataForm';
import MockFormikContext from './MockFormikContext';

describe('Test MovieDataForm', () => {
  beforeEach(() =>
    render(
      <MockFormikContext>
        <MovieDataForm />
      </MockFormikContext>
    )
  );

  it('Loads the series into the MovieDataForm series select box', async () => {
    const elementSeriesStarWars = await screen.findByRole('option', {
      name: 'Star Wars',
    });
    expect(elementSeriesStarWars).toBeInTheDocument();
  });

  it('Loads the studios into the MovieDataForm studio select box', async () => {
    const elementStudioWarnerBros = await screen.findByRole('option', {
      name: 'Warner Bros',
    });
    expect(elementStudioWarnerBros).toBeInTheDocument();
  });

  it('Has all form elements disabled on first load', async () => {
    expect(screen.getByRole('button', { name: /update/i })).toBeDisabled();
    expect(screen.getByRole('button', { name: /remove/i })).toBeDisabled();

    expect(
      await screen.findByRole('combobox', { name: 'Series' })
    ).toBeDisabled();
    expect(
      await screen.findByRole('combobox', { name: 'Studio' })
    ).toBeDisabled();

    // 2 textboxes - Name and Series #
    const textboxes = screen.getAllByRole('textbox');
    expect(textboxes.length).toBe(2);
    textboxes.forEach((textbox) => expect(textbox).toBeDisabled());

    //// 2 comboboxes - Series and Studio
    //const comboboxes = await screen.findAllByRole('combobox');
    //expect(comboboxes.length).toBe(2);
    //comboboxes.forEach((combobox) => expect(combobox).toBeDisabled());
  });
});
