import '@testing-library/jest-dom';
import { render, screen } from '../../test-utils';
import CategorySelector from '../CategorySelector';
import MockFormikContext from './MockFormikContext';

describe('Test CategorySelector', () => {
  beforeEach(() =>
    render(
      <MockFormikContext>
        <CategorySelector />
      </MockFormikContext>
    )
  );

  it('Loads the category into the CategorySelector', async () => {
    const elementCategoryHorror = await screen.findByRole('checkbox', {
      name: /horror/i,
    });
    expect(elementCategoryHorror).toBeInTheDocument();
  });

  it('Has all category checkboxes disabled upon first load', async () => {
    const checkBoxes = await screen.findAllByRole('checkbox');
    checkBoxes.forEach((checkbox) => expect(checkbox).toBeDisabled());
  });
});
