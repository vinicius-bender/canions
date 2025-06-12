document.addEventListener('DOMContentLoaded', () => {
  const sortSelect = document.getElementById('sortSelect');
  sortSelect.addEventListener('change', () => {
    document.getElementById('filterForm').submit();
  });
});