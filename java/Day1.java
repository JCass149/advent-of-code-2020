import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Scanner;

public class Day1 {

    public static void main(String[] args) {

        int target = 2020;

        ArrayList<Integer> arrayList = new ArrayList<>();

        try {
            File file = new File("../input/day1.txt");
            Scanner scanner = new Scanner(file);
            while (scanner.hasNextLine()) {
                arrayList.add(scanner.nextInt());
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }

        int[] validPair = findPair(arrayList, target, 0);
        System.out.println("Solution 1: " + validPair[0] * validPair[1]);

        int[] validTriplet = findTriplet(arrayList, target);
        System.out.println("Solution 2: " + validTriplet[0] * validTriplet[1] * validTriplet[2]);

    }

    public static int[] findPair(ArrayList<Integer> numbers, int target, int from) {
        HashSet<Integer> seenSet = new HashSet<>();
        int[] toReturn = new int[2];
        for (int i = from; i < numbers.size(); i++) {
            if (seenSet.contains(target - numbers.get(i))) {
                int current = numbers.get(i);
                toReturn[0] = current;
                toReturn[1] = target - current;
                return toReturn;
            } else {
                seenSet.add(numbers.get(i));
            }
        }
        return null;
    }

    public static int[] findTriplet(ArrayList<Integer> numbers, int target) {
        int[] toReturn = new int[3];
        for (int i = 0; i < numbers.size(); i++) {

            int[] result = findPair(numbers, target - numbers.get(i), i);
            // if not null i.e. a pair found
            if (result != null) {
                toReturn[0] = numbers.get(i);
                toReturn[1] = result[0];
                toReturn[2] = result[1];
                return toReturn;

            }
        }
        return null;
    }

}