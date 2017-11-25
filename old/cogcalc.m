%WIP Not function
function [mass, cog] = cogcalc(masses, pos)

for row = 1:numel(masses)
    posmasstotal=0;
    for seat = 1:numel(masses(row))
        posmasstotal = posmasstotal + masses(row)
    end
end