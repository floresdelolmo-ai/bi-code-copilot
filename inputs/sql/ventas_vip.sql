-- Consulta de análisis de ventas por cliente VIP
SELECT 
    c.CategoryName,
    cust.CustomerName,
    SUM(od.Quantity * od.UnitPrice) as TotalVentas,
    COUNT(DISTINCT o.OrderID) as TotalPedidos
FROM Sales.Orders o
JOIN Sales.OrderDetails od ON o.OrderID = od.OrderID
JOIN Sales.Products p ON od.ProductID = p.ProductID
JOIN Sales.Categories c ON p.CategoryID = c.CategoryID
JOIN Sales.Customers cust ON o.CustomerID = cust.CustomerID
WHERE o.OrderDate >= '2026-01-01'
GROUP BY c.CategoryName, cust.CustomerName
HAVING SUM(od.Quantity * od.UnitPrice) > 15000
ORDER BY TotalVentas DESC;
