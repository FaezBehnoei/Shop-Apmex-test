export const formatNumber = (num) => {
  const parsed = Number(num)

  if (Number.isFinite(parsed)) {
    return new Intl.NumberFormat('fa-IR').format(parsed)
  }

  return ''
}
