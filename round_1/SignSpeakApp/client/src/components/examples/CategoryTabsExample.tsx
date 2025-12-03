import { useState } from 'react';
import CategoryTabs from '../CategoryTabs';

export default function CategoryTabsExample() {
  const [active, setActive] = useState('👥');

  return (
    <CategoryTabs
      activeCategory={active}
      onCategoryChange={setActive}
    />
  );
}
