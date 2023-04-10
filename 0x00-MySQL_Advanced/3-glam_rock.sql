-- A script that lists all bands with glam rock
SELECT bands_name, (IFNULL(split, '2002') - formed) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
