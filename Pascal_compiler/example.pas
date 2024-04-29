program LoopsExample;

var
  i, j: Integer;

begin
  // While loop example
  i := 1;
  while i <= 5 do
  begin
    writeln('While loop iteration ', i);
    Inc(i);
  end;

  // For loop example
  writeln(''); // Adding a newline for clarity
  for j := 1 to 5 do
  begin
    writeln('For loop iteration ', j);
  end;
end.
